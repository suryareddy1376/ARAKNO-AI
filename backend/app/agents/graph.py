"""
ARAKNO-AI Research Workflow Graph.
Executes the staged research pipeline:
Intake -> Literature Retrieval -> Protein Intelligence -> Evidence Extraction -> Citation Verification -> Report Synthesis.
"""

from typing import Callable, List
from app.agents.state import ResearchWorkflowState
from app.agents.nodes import (
    research_intake_node,
    literature_retrieval_node,
    protein_intelligence_node,
    evidence_extraction_node,
    citation_verification_node,
    report_generation_node,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


class ResearchWorkflowGraph:
    """Deterministic, traceable scientific research pipeline."""

    def __init__(self):
        self.nodes = [
            ("intake", research_intake_node, 0.15),
            ("retrieval", literature_retrieval_node, 0.40),
            ("protein", protein_intelligence_node, 0.60),
            ("evidence", evidence_extraction_node, 0.75),
            ("citation", citation_verification_node, 0.85),
            ("report", report_generation_node, 1.0),
        ]

    async def execute(
        self,
        state: ResearchWorkflowState,
        progress_callback: Callable[[str, float], None] = None,
    ) -> ResearchWorkflowState:
        """Run all pipeline nodes sequentially, reporting progress."""
        for node_name, node_func, progress in self.nodes:
            try:
                if progress_callback:
                    await progress_callback(node_name, progress)
                state = await node_func(state)
            except Exception as e:
                logger.error(f"Error in research node {node_name}", error=str(e))
                state.error = f"Node {node_name} encountered error: {str(e)}"
                state.execution_log.append(f"Error in {node_name}: {str(e)}")

        return state
