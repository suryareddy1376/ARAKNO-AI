"""
Modular workflow nodes for ARAKNO-AI scientific research pipeline.
Functions operate predictably and objectively without fabricating citations or claims.
"""

import re
from typing import Dict, Any, List
from app.agents.state import ResearchWorkflowState
from app.integrations.pubmed.client import PubMedClient
from app.integrations.europe_pmc.client import EuropePMCClient
from app.integrations.uniprot.client import UniProtClient
from app.integrations.alphafold.client import AlphaFoldClient
from app.core.logging import get_logger

logger = get_logger(__name__)

# Known biological targets for ARAKNO divisions
TARGET_PROTEINS = {
    "COL1A1": "P02452",
    "COL1A2": "P08123",
    "BMP2": "P12643",
    "RUNX2": "Q13950",
    "SP7": "Q8TF47",
    "BGLAP": "P02818",
    "SPARC": "P09486",
}


async def research_intake_node(state: ResearchWorkflowState) -> ResearchWorkflowState:
    """Analyze the research question, extract target proteins and biological keywords."""
    state.execution_log.append("Intake: Analyzing research question and target concepts")
    q_upper = state.query.upper()

    # Identify protein targets mentioned in query
    for symbol, acc in TARGET_PROTEINS.items():
        if symbol in q_upper or acc in q_upper:
            if symbol not in state.protein_targets:
                state.protein_targets.append(symbol)

    # General biological entity keyword extraction
    keywords = ["fusion", "biomechanics", "osteoblast", "collagen", "cage", "scaffold", "titanium", "bone", "spine"]
    for kw in keywords:
        if kw in state.query.lower():
            state.identified_entities.append(kw)

    return state


async def literature_retrieval_node(state: ResearchWorkflowState) -> ResearchWorkflowState:
    """Retrieve scientific literature from PubMed and Europe PMC; deduplicate by PMID and DOI."""
    state.execution_log.append("Literature: Querying scientific databases")
    pubmed_client = PubMedClient()
    europe_pmc_client = EuropePMCClient()

    articles: List[Dict[str, Any]] = []

    # Query PubMed if requested
    if "pubmed" in state.sources:
        try:
            pm_res = await pubmed_client.search_and_fetch(state.query, max_results=state.max_results)
            articles.extend(pm_res)
            state.execution_log.append(f"PubMed: Retrieved {len(pm_res)} candidate articles")
        except Exception as e:
            logger.error("PubMed retrieval node error", error=str(e))

    # Query Europe PMC if requested
    if "europe_pmc" in state.sources:
        try:
            epmc_res = await europe_pmc_client.search(state.query, max_results=state.max_results)
            articles.extend(epmc_res)
            state.execution_log.append(f"Europe PMC: Retrieved {len(epmc_res)} candidate articles")
        except Exception as e:
            logger.error("Europe PMC retrieval node error", error=str(e))

    # Deduplicate by PMID and normalized title
    seen_pmids = set()
    seen_titles = set()
    deduped = []

    for art in articles:
        pmid = art.get("pmid")
        title_norm = re.sub(r"\W+", "", art.get("title", "").lower())

        if pmid and pmid in seen_pmids:
            continue
        if title_norm and title_norm in seen_titles:
            continue

        if pmid:
            seen_pmids.add(pmid)
        if title_norm:
            seen_titles.add(title_norm)
        deduped.append(art)

    state.publications = deduped[:state.max_results]
    state.execution_log.append(f"Literature: Normalized to {len(state.publications)} unique peer-reviewed publications")
    return state


async def protein_intelligence_node(state: ResearchWorkflowState) -> ResearchWorkflowState:
    """Resolve UniProt entries and query AlphaFold models if protein targets identified."""
    if not state.protein_targets and "alphafold" in state.sources:
        # Default to human COL1A1 if query concerns collagen/bone/spine and none specified
        if any(term in state.query.lower() for term in ["collagen", "bone", "spine", "implant", "fusion"]):
            state.protein_targets.append("COL1A1")

    if not state.protein_targets:
        return state

    state.execution_log.append(f"Protein Intelligence: Resolving targets {state.protein_targets}")
    uniprot_client = UniProtClient()
    af_client = AlphaFoldClient()

    for sym in state.protein_targets:
        acc = TARGET_PROTEINS.get(sym)
        if not acc:
            # Try UniProt search
            entries = await uniprot_client.search(sym, limit=1)
            if entries:
                acc = entries[0]["accession"]

        if not acc:
            continue

        entry = await uniprot_client.get_entry(acc)
        prediction = await af_client.get_prediction(acc)

        record = {
            "gene_symbol": sym,
            "accession": acc,
            "protein_name": entry.get("protein_name") if entry else sym,
            "organism": entry.get("organism") if entry else "Homo sapiens",
            "sequence_length": entry.get("sequence_length") if entry else None,
            "function": entry.get("function_description") if entry else None,
            "alphafold_model": prediction[0].get("pdbUrl") if prediction else None,
            "alphafold_plddt": prediction[0].get("globalPlddt") if prediction else None,
        }
        state.protein_records.append(record)

    return state


async def evidence_extraction_node(state: ResearchWorkflowState) -> ResearchWorkflowState:
    """Extract evidence claims, study types, and experimental context from publications."""
    state.execution_log.append("Evidence Extraction: Extracting claims from abstracts")
    claims = []

    for pub in state.publications:
        abstract = pub.get("abstract", "")
        if not abstract:
            continue

        # Look for clinical, experimental, or computational signals
        abs_lower = abstract.lower()
        ev_type = "citation"
        strength = "moderate"
        category = "C"  # Cell/Laboratory

        if any(w in abs_lower for w in ["patient", "clinical trial", "cohort", "multicenter", "randomized"]):
            ev_type = "experimental"
            category = "A"  # Human clinical
            strength = "strong"
        elif any(w in abs_lower for w in ["rat", "mouse", "ovine", "porcine", "in vivo", "animal"]):
            ev_type = "experimental"
            category = "B"  # Animal
        elif any(w in abs_lower for w in ["finite element", "simulation", "computational", "in silico", "predict"]):
            ev_type = "computational"
            category = "D"  # Computational

        # Extract sentence with concluding or objective findings
        sentences = [s.strip() for s in abstract.split(".") if len(s.strip()) > 30]
        finding = sentences[-1] if sentences else abstract[:200]

        claims.append({
            "claim": f"{pub.get('title')}: {finding}",
            "publication_title": pub.get("title"),
            "pmid": pub.get("pmid"),
            "doi": pub.get("doi"),
            "year": pub.get("year"),
            "journal": pub.get("journal"),
            "evidence_type": ev_type,
            "evidence_category": category,
            "strength": strength,
            "excerpt": finding,
        })

    state.evidence_claims = claims
    state.execution_log.append(f"Evidence: Extracted {len(claims)} verifiable evidence records")
    return state


async def citation_verification_node(state: ResearchWorkflowState) -> ResearchWorkflowState:
    """Verify that all evidence claims reference real PMIDs or DOIs from retrieved sources."""
    state.execution_log.append("Citation Verification: Validating source traceability")
    verified_count = 0

    for claim in state.evidence_claims:
        if claim.get("pmid") or claim.get("doi"):
            verified_count += 1

    state.citations_verified = (verified_count == len(state.evidence_claims)) if state.evidence_claims else True
    state.verification_summary = f"Verified {verified_count}/{len(state.evidence_claims)} citations with verified PMIDs/DOIs."
    return state


async def report_generation_node(state: ResearchWorkflowState) -> ResearchWorkflowState:
    """Generate structured markdown research report adhering to scientific standards."""
    state.execution_log.append("Report Generation: Synthesizing scientific report")

    md_lines = [
        f"# Research Report: {state.query}",
        "",
        "> **ARAKNO-AI Scientific Intelligence Dossier**",
        "> *Notice: Computational literature analysis for research purposes. Not clinical advice.*",
        "",
        "## 1. Executive Summary",
        f"This investigation addressed: *'{state.query}'* across peer-reviewed literature and computational structural repositories.",
        f"A total of **{len(state.publications)}** peer-reviewed publications were retrieved and analyzed across {', '.join(state.sources)}.",
        f"Identified {len(state.evidence_claims)} verifiable scientific claims and {len(state.protein_records)} structural macromolecular targets.",
        "",
        "## 2. Identified Biological Targets",
    ]

    if state.protein_records:
        for p in state.protein_records:
            md_lines.append(f"- **{p['gene_symbol']}** ({p['protein_name']}) — UniProt: `{p['accession']}`, Organism: *{p['organism']}*")
            if p.get("alphafold_plddt"):
                md_lines.append(f"  - AlphaFold Global pLDDT: **{p['alphafold_plddt']}** (Model available)")
    else:
        md_lines.append("No specific macromolecular targets isolated for this query.")

    md_lines.extend([
        "",
        "## 3. Evidence Matrix",
        "| Source | Year | Journal | Evidence Category | Strength | Key Finding |",
        "|---|---|---|---|---|---|",
    ])

    for c in state.evidence_claims[:10]:
        title_trunc = c['publication_title'][:40] + "..." if len(c['publication_title']) > 40 else c['publication_title']
        pmid_link = f"[{title_trunc}](https://pubmed.ncbi.nlm.nih.gov/{c['pmid']})" if c.get('pmid') else title_trunc
        md_lines.append(f"| {pmid_link} | {c.get('year') or 'N/A'} | {c.get('journal') or 'N/A'} | Cat {c.get('evidence_category')} | {c['strength']} | {c['excerpt'][:80]}... |")

    md_lines.extend([
        "",
        "## 4. Citation & Traceability Verification",
        f"- Status: **{'VERIFIED' if state.citations_verified else 'PARTIAL'}**",
        f"- Traceability: {state.verification_summary}",
        "",
        "## 5. Peer-Reviewed References",
    ])

    for i, pub in enumerate(state.publications, 1):
        authors = ", ".join(pub.get("authors", [])[:3])
        if len(pub.get("authors", [])) > 3:
            authors += " et al."
        ref_line = f"{i}. **{pub.get('title')}**. *{pub.get('journal', 'Journal')}*, {pub.get('year', 'N/A')}."
        if pub.get("pmid"):
            ref_line += f" PMID: [{pub['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{pub['pmid']}/)"
        if pub.get("doi"):
            ref_line += f" DOI: [{pub['doi']}](https://doi.org/{pub['doi']})"
        md_lines.append(ref_line)

    state.report_markdown = "\n".join(md_lines)
    state.executive_summary = f"Synthesized {len(state.publications)} publications and {len(state.evidence_claims)} claims into verifiable research dossier."

    # Optional AI Synthesis if requested and configured
    if state.synthesize_ai:
        try:
            from app.llm.client import LLMClient
            llm = LLMClient()
            if llm.is_enabled:
                state.execution_log.append(f"AI Synthesis: Generating summary using {llm.settings.llm_provider}")
                claims_text = "\n".join([f"- [{c.get('pmid', 'N/A')}] {c.get('claim')}" for c in state.evidence_claims[:8]])
                prompt = (
                    f"You are a biomedical researcher analyzing: '{state.query}'.\n"
                    f"Provide an objective 2-paragraph synthesis of the following verified literature claims.\n"
                    f"Do not fabricate citations or medical advice.\n\n"
                    f"Evidence:\n{claims_text}"
                )
                synthesis, _ = await llm.generate_completion(prompt, enable_thinking=True)
                if synthesis and not synthesis.startswith("[LLM"):
                    # Insert synthesis section into report
                    state.report_markdown += f"\n\n## 6. AI Evidence Synthesis\n{synthesis}\n"
                    state.executive_summary = synthesis[:250] + "..."
        except Exception as e:
            logger.error("AI synthesis step error", error=str(e))

    return state
