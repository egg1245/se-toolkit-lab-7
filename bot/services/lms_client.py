"""LMS API client for task-2.

HTTP client for querying the LMS backend using Bearer token authentication.
"""

from typing import Any

import httpx


class LMSClient:
    """Client for LMS REST API.
    
    Handles authentication, error handling, and timeouts.
    """

    def __init__(self, base_url: str, api_key: str, timeout: int = 5):
        """Initialize LMS client.
        
        Args:
            base_url: Base URL of LMS API (e.g., "http://backend:42002").
            api_key: Bearer token for authentication.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        """Build request headers with Bearer token.
        
        Returns:
            Headers dict with Authorization.
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def get_items(self) -> list[dict[str, Any]]:
        """Fetch items from LMS.
        
        Returns:
            List of items.
            
        Raises:
            httpx.HTTPError: On network or server error.
        """
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/items/"
            response = await client.get(url, headers=self._headers(), timeout=self.timeout)
            response.raise_for_status()
            return response.json()

    async def get_labs(self) -> list[dict[str, Any]]:
        """Fetch labs from LMS.
        
        Returns:
            List of lab objects.
            
        Raises:
            httpx.HTTPError: On network or server error.
        """
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/labs/"
            response = await client.get(url, headers=self._headers(), timeout=self.timeout)
            response.raise_for_status()
            return response.json()

    async def get_scores(self, user_id: str | None = None) -> dict[str, Any]:
        """Fetch user scores from LMS.
        
        Args:
            user_id: Optional user ID. If None, returns current user's scores.
            
        Returns:
            Scores object.
            
        Raises:
            httpx.HTTPError: On network or server error.
        """
        endpoint = f"/scores/{user_id}" if user_id else "/scores/"
        
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{endpoint}"
            response = await client.get(url, headers=self._headers(), timeout=self.timeout)
            response.raise_for_status()
            return response.json()
