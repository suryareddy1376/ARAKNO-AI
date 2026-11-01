"""
Europe PMC REST API client.
Provides literature search, full-text links, and open-access metadata.
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
import httpx

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class EuropePMCClient:
    """Client for Europe PMC REST API."""

    BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest"

    def __init__(self):
        self.settings = get_settings()
        self._last_request_time = 0.0
        self._min_interval = 0.20  # Max 5 req/sec

    async def _rate_limit(self):
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < self._min_interval:
            await asyncio.sleep(self._min_interval - elapsed)
        self._last_request_time = time.time()

    async def search(
        self,
        query: str,
        max_results: int = 20,
        open_access_only: bool = False,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Search Europe PMC publications."""
        await self._rate_limit()

        search_query = query
        if open_access_only:
            search_query += " OPEN_ACCESS:y"
        if year_start and year_end:
            search_query += f" PUB_YEAR:[{year_start} TO {year_end}]"
        elif year_start:
            search_query += f" PUB_YEAR:[{year_start} TO 2099]"
        elif year_end:
            search_query += f" PUB_YEAR:[1900 TO {year_end}]"

        params = {
            "query": search_query,
            "format": "json",
            "pageSize": str(min(max_results, 100)),
            "resultType": "core",
        }

        url = f"{self.BASE_URL}/search"
        try:
            async with httpx.AsyncClient(timeout=self.settings.default_timeout) as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()

                result_list = data.get("resultList", {}).get("result", [])
                articles = []

                for item in result_list:
                    # Parse authors
                    author_string = item.get("authorString", "")
                    authors = [a.strip() for a in author_string.split(",") if a.strip()]

                    # Extract year
                    pub_year = None
                    try:
                        pub_year = int(item.get("pubYear", 0)) if item.get("pubYear") else None
                    except (ValueError, TypeError):
                        pass

                    pmid = item.get("pmid")
                    pmcid = item.get("pmcid")
                    doi = item.get("doi")

                    articles.append({
                        "pmid": pmid,
                        "pmc_id": pmcid,
                        "doi": doi,
                        "title": item.get("title", "").rstrip("."),
                        "authors": authors,
                        "journal": item.get("journalTitle", ""),
                        "year": pub_year,
                        "abstract": item.get("abstractText", ""),
                        "publication_type": item.get("pubType", None),
                        "source": "europe_pmc",
                        "url": f"https://europepmc.org/article/{'MED' if pmid else 'PMC'}/{pmid or pmcid}" if (pmid or pmcid) else None,
                        "is_open_access": item.get("isOpenAccess") == "Y",
                        "citation_count": item.get("citedByCount", 0),
                    })
                return articles
        except Exception as e:
            logger.error("Europe PMC search error", error=str(e), query=query)
            return []
