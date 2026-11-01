"""
UniProt REST API client.
Official documentation: https://www.uniprot.org/help/api
Endpoints:
  - Search: https://rest.uniprot.org/uniprotkb/search
  - Entry: https://rest.uniprot.org/uniprotkb/{accession}
"""

from typing import List, Dict, Any, Optional
import httpx

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class UniProtClient:
    """Client for UniProt REST API."""

    BASE_URL = "https://rest.uniprot.org/uniprotkb"

    def __init__(self):
        self.settings = get_settings()

    async def get_entry(self, accession: str) -> Optional[Dict[str, Any]]:
        """Fetch UniProt entry metadata and sequence by accession."""
        clean_acc = accession.strip().upper()
        url = f"{self.BASE_URL}/{clean_acc}"
        params = {"format": "json"}

        try:
            async with httpx.AsyncClient(timeout=self.settings.default_timeout) as client:
                resp = await client.get(url, params=params)
                if resp.status_code == 404:
                    return None
                resp.raise_for_status()
                data = resp.json()
                return self._parse_entry(data)
        except Exception as e:
            logger.error("UniProt get_entry error", error=str(e), accession=clean_acc)
            return None

    async def search(self, query: str, organism: Optional[str] = "Homo sapiens", limit: int = 10) -> List[Dict[str, Any]]:
        """Search UniProt entries by gene, protein name, or keyword."""
        clean_q = query.strip()

        # Prioritize reviewed Swiss-Prot canonical entries with exact gene symbol matches
        if organism:
            prioritized_query = f"(gene_exact:{clean_q} OR gene:{clean_q} OR {clean_q}) AND (organism_name:\"{organism}\" OR taxonomy_id:9606) AND (reviewed:true)"
        else:
            prioritized_query = f"(gene_exact:{clean_q} OR {clean_q}) AND (reviewed:true)"

        url = f"{self.BASE_URL}/search"
        try:
            async with httpx.AsyncClient(timeout=self.settings.default_timeout) as client:
                # 1. Try prioritized reviewed search
                resp = await client.get(url, params={"query": prioritized_query, "format": "json", "size": str(min(limit, 25))})
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("results", [])
                    if results:
                        return [self._parse_entry(item) for item in results if item]

                # 2. Fallback to broad search if no reviewed entry found
                fallback_query = clean_q
                if organism:
                    fallback_query = f"{fallback_query} AND (organism_name:\"{organism}\" OR taxonomy_id:9606)"
                resp2 = await client.get(url, params={"query": fallback_query, "format": "json", "size": str(min(limit, 25))})
                if resp2.status_code == 200:
                    data2 = resp2.json()
                    results2 = data2.get("results", [])
                    return [self._parse_entry(item) for item in results2 if item]
        except Exception as e:
            logger.error("UniProt search error", error=str(e), query=query)

        return []

    def _parse_entry(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize UniProt API response into a clean dictionary."""
        primary_acc = data.get("primaryAccession", "")
        entry_name = data.get("uniProtkbId", "")

        # Protein name
        protein_desc = data.get("proteinDescription", {})
        rec_name = protein_desc.get("recommendedName", {}).get("fullName", {}).get("value", "")
        if not rec_name:
            sub_names = protein_desc.get("submissionNames", [])
            if sub_names:
                rec_name = sub_names[0].get("fullName", {}).get("value", "")

        # Gene symbol
        genes = data.get("genes", [])
        gene_symbol = None
        if genes:
            gene_symbol = genes[0].get("geneName", {}).get("value", "")

        # Organism
        organism_data = data.get("organism", {})
        organism_name = organism_data.get("scientificName", "")
        taxon_id = organism_data.get("taxonId", None)

        # Sequence
        sequence_data = data.get("sequence", {})
        sequence = sequence_data.get("value", "")
        seq_length = sequence_data.get("length", len(sequence))

        # Function comments
        function_desc = []
        for comment in data.get("comments", []):
            if comment.get("commentType") == "FUNCTION":
                for text_item in comment.get("texts", []):
                    function_desc.append(text_item.get("value", ""))
        function_text = "\n\n".join(function_desc) if function_desc else None

        # GO terms
        go_terms = []
        for xref in data.get("uniProtKBCrossReferences", []):
            if xref.get("database") == "GO":
                props = {p.get("key"): p.get("value") for p in xref.get("properties", [])}
                go_terms.append({
                    "id": xref.get("id"),
                    "term": props.get("GoTerm", ""),
                })

        return {
            "accession": primary_acc,
            "entry_name": entry_name,
            "protein_name": rec_name,
            "gene_name": gene_symbol,
            "organism": organism_name,
            "organism_id": taxon_id,
            "sequence": sequence,
            "sequence_length": seq_length,
            "function_description": function_text,
            "go_terms": go_terms,
            "annotation_score": data.get("annotationScore", None),
        }
