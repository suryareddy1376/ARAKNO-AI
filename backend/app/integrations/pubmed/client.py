"""
PubMed NCBI E-Utilities API client.
Supports ESearch, ESummary, and EFetch with rate limiting and robust error handling.
"""

import asyncio
import time
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
import httpx

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class PubMedClient:
    """Client for NCBI E-Utilities (PubMed)."""

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self):
        self.settings = get_settings()
        self._last_request_time = 0.0
        # NCBI rate limits: 3 req/sec without API key, 10 req/sec with key
        self._min_interval = 0.35 if not self.settings.ncbi_api_key else 0.11

    async def _rate_limit(self):
        """Enforce NCBI rate limits."""
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < self._min_interval:
            await asyncio.sleep(self._min_interval - elapsed)
        self._last_request_time = time.time()

    def _get_base_params(self) -> Dict[str, str]:
        params = {"tool": "ARAKNO-AI"}
        if self.settings.ncbi_email:
            params["email"] = self.settings.ncbi_email
        if self.settings.ncbi_api_key:
            params["api_key"] = self.settings.ncbi_api_key
        return params

    async def search(
        self,
        term: str,
        max_results: int = 20,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
    ) -> List[str]:
        """Search PubMed and return a list of PMIDs."""
        await self._rate_limit()

        query = term
        if year_start and year_end:
            query += f" AND {year_start}:{year_end}[dp]"
        elif year_start:
            query += f" AND {year_start}:3000[dp]"
        elif year_end:
            query += f" AND 1800:{year_end}[dp]"

        params = {
            **self._get_base_params(),
            "db": "pubmed",
            "term": query,
            "retmax": str(max_results),
            "retmode": "json",
            "sort": "pub_date",
        }

        url = f"{self.BASE_URL}/esearch.fcgi"
        try:
            async with httpx.AsyncClient(timeout=self.settings.default_timeout) as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                id_list = data.get("esearchresult", {}).get("idlist", [])
                return id_list
        except Exception as e:
            logger.error("PubMed search error", error=str(e), term=term)
            return []

    async def fetch_summaries(self, pmids: List[str]) -> List[Dict[str, Any]]:
        """Fetch publication summaries for a list of PMIDs using ESummary."""
        if not pmids:
            return []

        await self._rate_limit()
        params = {
            **self._get_base_params(),
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "json",
        }

        url = f"{self.BASE_URL}/esummary.fcgi"
        try:
            async with httpx.AsyncClient(timeout=self.settings.default_timeout) as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                result_dict = data.get("result", {})
                
                results = []
                for pmid in pmids:
                    item = result_dict.get(pmid)
                    if not item:
                        continue
                    
                    authors = [a.get("name", "") for a in item.get("authors", []) if "name" in a]
                    pub_date = item.get("pubdate", "")
                    year = None
                    if pub_date:
                        parts = pub_date.split()
                        if parts and parts[0].isdigit():
                            year = int(parts[0])

                    article_ids = item.get("articleids", [])
                    doi = None
                    pmc = None
                    for aid in article_ids:
                        if aid.get("idtype") == "doi":
                            doi = aid.get("value")
                        elif aid.get("idtype") == "pmc":
                            pmc = aid.get("value")

                    results.append({
                        "pmid": pmid,
                        "title": item.get("title", "").rstrip("."),
                        "authors": authors,
                        "journal": item.get("source", ""),
                        "year": year,
                        "doi": doi,
                        "pmc_id": pmc,
                        "publication_type": item.get("pubtype", [None])[0] if item.get("pubtype") else None,
                        "source": "pubmed",
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    })
                return results
        except Exception as e:
            logger.error("PubMed summary fetch error", error=str(e), pmids=pmids)
            return []

    async def fetch_abstracts(self, pmids: List[str]) -> Dict[str, str]:
        """Fetch abstracts for PMIDs using EFetch (XML)."""
        if not pmids:
            return {}

        await self._rate_limit()
        params = {
            **self._get_base_params(),
            "db": "pubmed",
            "id": ",".join(pmids[:50]),  # Fetch up to 50 at once
            "retmode": "xml",
        }

        url = f"{self.BASE_URL}/efetch.fcgi"
        abstracts = {}
        try:
            async with httpx.AsyncClient(timeout=self.settings.default_timeout) as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                root = ET.fromstring(resp.content)
                
                for article in root.findall(".//PubmedArticle"):
                    pmid_elem = article.find(".//PMID")
                    if pmid_elem is None or not pmid_elem.text:
                        continue
                    pmid = pmid_elem.text
                    
                    abs_texts = []
                    for abs_elem in article.findall(".//AbstractText"):
                        label = abs_elem.get("Label")
                        text = "".join(abs_elem.itertext()).strip()
                        if label:
                            abs_texts.append(f"{label}: {text}")
                        elif text:
                            abs_texts.append(text)
                    
                    if abs_texts:
                        abstracts[pmid] = "\n\n".join(abs_texts)
        except Exception as e:
            logger.error("PubMed abstract fetch error", error=str(e))
        return abstracts

    async def search_and_fetch(
        self,
        query: str,
        max_results: int = 20,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Search PubMed and fetch complete records including abstracts."""
        pmids = await self.search(query, max_results=max_results, year_start=year_start, year_end=year_end)
        if not pmids:
            return []

        summaries = await self.fetch_summaries(pmids)
        abstracts = await self.fetch_abstracts(pmids)

        for s in summaries:
            s["abstract"] = abstracts.get(s["pmid"], "")

        return summaries
