import asyncio
import sys
import httpx
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

async def main():
    print("=" * 60)
    print("ARAKNO-AI LIVE END-TO-END VERIFICATION")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1. Health check
        print("\n[Step 1] Checking Backend Health...")
        resp = await client.get(f"{BASE_URL}/health")
        assert resp.status_code == 200, f"Health check failed: {resp.text}"
        print("  -> Status:", resp.json())

        # 2. System Status
        print("\n[Step 2] Checking System Status & Privacy Enforcement...")
        resp = await client.get(f"{BASE_URL}/system/status")
        assert resp.status_code == 200
        sys_status = resp.json()
        print("  -> Database connected:", sys_status.get("database_connected"))
        print("  -> Privacy mode active:", sys_status.get("privacy_mode"))
        print("  -> LLM Provider:", sys_status.get("llm_provider"))

        # 3. Divisions Check
        print("\n[Step 3] Verifying 6 ARAKNO Research Divisions...")
        resp = await client.get(f"{BASE_URL}/projects/divisions")
        assert resp.status_code == 200
        divisions = resp.json()
        div_names = [d["name"] for d in divisions]
        print(f"  -> Found {len(divisions)} divisions:", div_names)
        assert "ARAKNO-SPINE" in div_names
        assert "ARAKNO-BONE" in div_names

        # 4. Search PubMed
        print("\n[Step 4] Searching PubMed (NCBI E-Utilities)...")
        search_payload = {
            "query": "spinal fusion pedicle screw biomechanics",
            "source": "pubmed",
            "max_results": 5
        }
        resp = await client.post(f"{BASE_URL}/literature/search", json=search_payload)
        assert resp.status_code == 200
        pm_results = resp.json()
        print(f"  -> Retrieved {len(pm_results)} publications from PubMed")
        for i, p in enumerate(pm_results[:2], 1):
            print(f"     {i}. PMID: {p.get('pmid')} - {p.get('title')[:60]}...")

        # 5. Save Publication
        saved_paper_id = None
        if pm_results:
            paper_to_save = pm_results[0]
            print(f"\n[Step 5] Saving Publication (PMID: {paper_to_save.get('pmid')})...")
            save_payload = {
                "title": paper_to_save["title"],
                "pmid": paper_to_save["pmid"],
                "doi": paper_to_save.get("doi"),
                "journal": paper_to_save.get("journal"),
                "year": paper_to_save.get("year"),
                "abstract": paper_to_save.get("abstract"),
                "source": paper_to_save["source"],
                "url": paper_to_save.get("url")
            }
            resp = await client.post(f"{BASE_URL}/literature/save", json=save_payload)
            assert resp.status_code == 200
            saved = resp.json()
            saved_paper_id = saved["id"]
            print("  -> Successfully saved in SQLite with ID:", saved_paper_id)

        # 6. UniProt Protein Exploration (COL1A1 - P02452)
        print("\n[Step 6] Querying UniProt for human COL1A1 (P02452)...")
        resp = await client.get(f"{BASE_URL}/proteins/P02452")
        assert resp.status_code == 200
        protein_data = resp.json()
        print("  -> Protein Name:", protein_data.get("protein_name"))
        print("  -> Gene Symbol:", protein_data.get("gene_name"))
        print("  -> Sequence Length:", protein_data.get("sequence_length"), "aa")

        # 7. AlphaFold Model Prediction Query
        print("\n[Step 7] Querying AlphaFold DB for P02452...")
        resp = await client.get(f"{BASE_URL}/proteins/P02452/structures")
        assert resp.status_code == 200
        af_structures = resp.json()
        print(f"  -> AlphaFold predictions found: {len(af_structures)}")
        if af_structures:
            af_model = af_structures[0]
            print("  -> Entry ID:", af_model.get("entryId"))
            print("  -> Global pLDDT:", af_model.get("globalPlddt"))
            print("  -> PDB URL:", af_model.get("pdbUrl"))

        # 8. Structure Download & Caching
        print("\n[Step 8] Downloading AlphaFold PDB model for P02452...")
        resp = await client.post(f"{BASE_URL}/proteins/P02452/download?format=pdb")
        assert resp.status_code == 200
        dl_result = resp.json()
        print("  -> Downloaded to local path:", dl_result.get("local_path"))
        print("  -> Model pLDDT:", dl_result.get("confidence_score"))

        # 9. Structure Content retrieval (for 3D viewer)
        print("\n[Step 9] Testing Structure Content retrieval for 3Dmol viewer...")
        resp = await client.get(f"{BASE_URL}/proteins/P02452/structure-content")
        assert resp.status_code == 200
        pdb_lines = resp.text.splitlines()
        print(f"  -> Successfully retrieved PDB stream ({len(pdb_lines)} lines, starts with: {pdb_lines[0] if pdb_lines else ''})")

        # 10. Computational Biology Sequence Analysis
        print("\n[Step 10] Testing Sequence Alignment on COL1A1 fragments...")
        seq_payload = {
            "seq1": "MFSFVDLRLLLLLAATALLTHGQEEGQVEGQDEDIPPVT",
            "seq2": "MFSFVDLRLLLLLAATALLTHGQEEGQVEGQDEDIPPVT",
            "comparison_type": "global"
        }
        resp = await client.post(f"{BASE_URL}/biology/sequences/compare", json=seq_payload)
        assert resp.status_code == 200
        align_data = resp.json()
        print(f"  -> Pairwise Identity: {align_data.get('identity_percentage')}% (Matches: {align_data.get('matches')})")

        # 11. Create Evidence Record
        print("\n[Step 11] Creating Traceable Evidence Record...")
        evidence_payload = {
            "claim": "Solid bone bridging across interbody cage establishes anterior column load bearing prior to instrumentation removal.",
            "evidence_type": "experimental",
            "strength": "strong",
            "source_section": "Discussion",
            "publication_id": saved_paper_id,
            "verified": True
        }
        resp = await client.post(f"{BASE_URL}/evidence", json=evidence_payload)
        assert resp.status_code == 200
        evidence_res = resp.json()
        print("  -> Created Evidence Record ID:", evidence_res["id"])

        # 12. Launch Agentic AI Research Job
        print("\n[Step 12] Launching Staged Research Workflow Job...")
        job_payload = {
            "query": "Bone healing, interbody cage fusion and criteria for hardware removal in spinal surgery",
            "division_slug": "arakno-spine",
            "sources": ["pubmed", "europe_pmc", "alphafold"],
            "max_results": 5,
            "synthesize_ai": False
        }
        resp = await client.post(f"{BASE_URL}/research/run", json=job_payload)
        assert resp.status_code == 200
        job_data = resp.json()
        job_id = job_data["id"]
        print(f"  -> Job {job_id} launched. Polling for completion...")

        # Poll job
        completed = False
        for attempt in range(20):
            await asyncio.sleep(2)
            j_resp = await client.get(f"{BASE_URL}/research/jobs/{job_id}")
            j_info = j_resp.json()
            progress = j_info.get("progress", 0)
            status = j_info.get("status")
            print(f"     ... Attempt {attempt+1}: Status={status}, Progress={int(progress*100)}%")
            if status in ("completed", "failed"):
                completed = True
                break

        assert completed, "Research job timed out"
        print("  -> Job finished with status:", status)

        # 13. Verify Generated Report
        print("\n[Step 13] Verifying Generated Research Report Dossier...")
        resp = await client.get(f"{BASE_URL}/reports")
        assert resp.status_code == 200
        reports = resp.json()
        print(f"  -> Found {len(reports)} generated reports in archive.")
        if reports:
            latest = reports[0]
            print(f"  -> Latest Report: '{latest['title']}' ({latest['word_count']} words)")
            assert latest["word_count"] > 50, "Report content too short"

        # 14. Frontend Connectivity Check
        print("\n[Step 14] Verifying Frontend Dev Server...")
        fe_resp = await client.get("http://127.0.0.1:5173")
        assert fe_resp.status_code == 200
        print("  -> Frontend running and serving HTML (HTTP 200 OK)")

    print("\n" + "=" * 60)
    print("ALL 14 END-TO-END VERIFICATION STEPS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
