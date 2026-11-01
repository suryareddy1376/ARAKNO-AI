"""
AlphaFold Protein Structure Database REST API client.
Official endpoint: https://alphafold.ebi.ac.uk/api/prediction/{qualifier}
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import httpx

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class AlphaFoldClient:
    """Client for AlphaFold Protein Structure Database API."""

    BASE_URL = "https://alphafold.ebi.ac.uk/api"

    def __init__(self):
        self.settings = get_settings()

    async def get_prediction(self, qualifier: str) -> Optional[List[Dict[str, Any]]]:
        """
        Query AlphaFold prediction metadata for a UniProt accession or qualifier.
        qualifier: UniProt accession e.g. 'P02452' (human COL1A1)
        """
        url = f"{self.BASE_URL}/prediction/{qualifier.strip()}"
        try:
            async with httpx.AsyncClient(timeout=self.settings.default_timeout) as client:
                resp = await client.get(url)
                if resp.status_code == 404:
                    logger.info("No AlphaFold prediction found for qualifier", qualifier=qualifier)
                    return None
                resp.raise_for_status()
                data = resp.json()
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return [data]
                return None
        except Exception as e:
            logger.error("AlphaFold API request error", error=str(e), qualifier=qualifier)
            return None

    async def download_structure_file(
        self,
        url: str,
        dest_filename: str,
    ) -> Optional[str]:
        """
        Download a structure file (.pdb or .cif) securely to local structures directory.
        Returns the absolute local path if successful.
        """
        # Validate target file extension
        ext = Path(dest_filename).suffix.lower()
        if ext not in self.settings.allowed_structure_extensions:
            logger.error("Invalid structure file extension", ext=ext)
            return None

        # Ensure structures directory exists
        structures_dir = Path(self.settings.structures_dir).resolve()
        structures_dir.mkdir(parents=True, exist_ok=True)

        target_path = structures_dir / dest_filename
        # Check path traversal
        if not str(target_path).startswith(str(structures_dir)):
            logger.error("Path traversal detected", path=str(target_path))
            return None

        # If already downloaded, return path
        if target_path.exists() and target_path.stat().st_size > 0:
            return str(target_path)

        try:
            async with httpx.AsyncClient(timeout=self.settings.download_timeout) as client:
                resp = await client.get(url, follow_redirects=True)
                resp.raise_for_status()
                content = resp.content

                # Check max size
                if len(content) > self.settings.max_download_size_bytes:
                    logger.error("Downloaded structure exceeds maximum allowed size", size=len(content))
                    return None

                target_path.write_bytes(content)
                logger.info("Downloaded structure file", path=str(target_path), size=len(content))
                return str(target_path)
        except Exception as e:
            logger.error("Failed to download structure file", error=str(e), url=url)
            return None
