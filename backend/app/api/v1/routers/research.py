"""
Agentic research job execution and tracking API router.
Runs the workflow pipeline asynchronously in the background.
"""

import asyncio
import json
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db
from app.db.database import get_db_context
from app.db.models.models import ResearchJob, ResearchActivity, ResearchReport
from app.db.repositories.jobs import JobRepository
from app.agents.state import ResearchWorkflowState
from app.agents.graph import ResearchWorkflowGraph
from app.schemas.research import (
    ResearchRunRequest,
    ResearchJobRead,
    ResearchJobResult,
)
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/research", tags=["Research"])


async def run_research_pipeline_task(job_id: str, run_req: ResearchRunRequest):
    """Background task executing the research pipeline and writing results to database."""
    async with get_db_context() as db:
        job_repo = JobRepository(db)
        await job_repo.update_status(job_id, status="running", progress=0.05)
        await db.commit()

    state = ResearchWorkflowState(
        query=run_req.query,
        project_id=run_req.project_id,
        division_slug=run_req.division_slug,
        sources=run_req.sources,
        max_results=run_req.max_results,
        synthesize_ai=run_req.synthesize_ai,
    )

    async def update_progress(node_name: str, progress: float):
        async with get_db_context() as db:
            repo = JobRepository(db)
            await repo.update_status(job_id, status="running", progress=progress)
            await db.commit()

    graph = ResearchWorkflowGraph()
    final_state = await graph.execute(state, progress_callback=update_progress)

    # Save results to database
    async with get_db_context() as db:
        job_repo = JobRepository(db)
        status = "completed" if not final_state.error else "failed"

        result_payload = {
            "query": final_state.query,
            "publications_count": len(final_state.publications),
            "publications": final_state.publications,
            "proteins": final_state.protein_records,
            "evidence_records": final_state.evidence_claims,
            "citations_verified": final_state.citations_verified,
            "verification_summary": final_state.verification_summary,
            "executive_summary": final_state.executive_summary,
            "report_markdown": final_state.report_markdown,
            "execution_log": final_state.execution_log,
        }

        await job_repo.update_status(
            job_id,
            status=status,
            progress=1.0,
            result=json.dumps(result_payload),
            error_message=final_state.error,
        )

        # Automatically generate research report record if completed
        if status == "completed" and final_state.report_markdown:
            report = ResearchReport(
                project_id=run_req.project_id,
                title=f"Investigation: {run_req.query[:80]}",
                report_type="full",
                content=final_state.report_markdown,
                format="markdown",
                status="completed",
                word_count=len(final_state.report_markdown.split()),
            )
            db.add(report)

            activity = ResearchActivity(
                activity_type="research",
                description=f"Completed research job: '{run_req.query[:60]}'",
                entity_type="job",
                entity_id=job_id,
            )
            db.add(activity)

        await db.commit()


@router.post("/run", response_model=ResearchJobRead)
async def start_research_run(
    req: ResearchRunRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Initiate an autonomous research job across scientific repositories."""
    job_repo = JobRepository(db)
    job_id = str(uuid.uuid4())

    job = ResearchJob(
        id=job_id,
        job_type="full_research",
        query=req.query,
        parameters=json.dumps(req.model_dump()),
        status="pending",
        progress=0.0,
    )
    await job_repo.create(job)
    await db.commit()

    background_tasks.add_task(run_research_pipeline_task, job_id, req)
    return ResearchJobRead.model_validate(job)


@router.get("/jobs", response_model=List[ResearchJobRead])
async def list_research_jobs(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List recent research jobs."""
    repo = JobRepository(db)
    jobs, _ = await repo.list_jobs(status=status, limit=50)
    return [ResearchJobRead.model_validate(j) for j in jobs]


@router.get("/jobs/{job_id}", response_model=ResearchJobRead)
async def get_job_status(
    job_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Check the real-time execution status and progress of a research job."""
    repo = JobRepository(db)
    job = await repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Research job not found")
    return ResearchJobRead.model_validate(job)


@router.get("/jobs/{job_id}/results")
async def get_job_results(
    job_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve full synthesized results, publications, and evidence from a completed job."""
    repo = JobRepository(db)
    job = await repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Research job not found")

    if job.status != "completed":
        return {
            "job_id": job.id,
            "status": job.status,
            "progress": job.progress,
            "message": f"Job is currently {job.status}. Results not yet available.",
        }

    data = json.loads(job.result) if job.result else {}
    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "data": data,
    }


@router.post("/jobs/{job_id}/cancel")
async def cancel_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Cancel a pending or running research job."""
    repo = JobRepository(db)
    job = await repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Research job not found")

    await repo.update_status(job_id, status="cancelled")
    await db.commit()
    return {"success": True, "message": "Job cancelled"}
