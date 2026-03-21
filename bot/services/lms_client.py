"""LMS API client for task-2.

HTTP client for querying the LMS backend using Bearer token authentication.
Synchronous methods only - no async/await.
"""

from typing import Any

import httpx


class LMSClient:
    """Client for LMS REST API (synchronous).
    
    Handles authentication, error handling, and timeouts.
    All methods are synchronous (blocking).
    """

    def __init__(self, base_url: str, api_key: str, timeout: int = 5):
        """Initialize LMS client.
        
        Args:
            base_url: Base URL of LMS API (e.g., "http://localhost:42002").
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

    def get_items(self) -> list[dict[str, Any]]:
        """Fetch items from LMS.
        
        Returns:
            List of items.
        """
        try:
            with httpx.Client() as client:
                url = f"{self.base_url}/items/"
                import sys
                print(f"[LMS] GET {url}", file=sys.stderr)
                response = client.get(url, headers=self._headers(), timeout=self.timeout)
                response.raise_for_status()
                result = response.json()
                print(f"[LMS] GET {url} -> {len(result) if isinstance(result, list) else 'ok'}", file=sys.stderr)
                return result
        except Exception as e:
            import sys
            print(f"[LMS] GET {url} -> ERROR: {e}", file=sys.stderr)
            return []
    
    def get_learners(self) -> list[dict[str, Any]]:
        """Fetch learners from LMS (sync version).
        
        Returns:
            List of learners.
        """
        try:
            with httpx.Client() as client:
                url = f"{self.base_url}/learners/"
                import sys
                print(f"[LMS] GET {url}", file=sys.stderr)
                response = client.get(url, headers=self._headers(), timeout=self.timeout)
                response.raise_for_status()
                result = response.json()
                print(f"[LMS] GET {url} -> {len(result) if isinstance(result, list) else 'ok'}", file=sys.stderr)
                return result
        except Exception as e:
            import sys
            print(f"[LMS] GET {url} -> ERROR: {e}", file=sys.stderr)
            return []
    
    def get_scores(self, lab: str = "") -> dict | list:
        """Fetch score distribution for a lab (sync version).
        
        Args:
            lab: Lab identifier.
            
        Returns:
            Score data.
        """
        try:
            with httpx.Client() as client:
                url = f"{self.base_url}/analytics/scores"
                params = {"lab": lab} if lab else {}
                response = client.get(url, headers=self._headers(), params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
        except Exception:
            return {}
    
    def get_pass_rates(self, lab: str = "") -> list:
        """Fetch pass rates for a lab (sync version).
        
        Args:
            lab: Lab identifier.
            
        Returns:
            Pass rate data.
        """
        try:
            with httpx.Client() as client:
                url = f"{self.base_url}/analytics/pass-rates"
                params = {"lab": lab} if lab else {}
                response = client.get(url, headers=self._headers(), params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
        except Exception:
            return []
    
    def get_timeline(self, lab: str = "") -> list:
        """Fetch submission timeline for a lab (sync version).
        
        Args:
            lab: Lab identifier.
            
        Returns:
            Timeline data.
        """
        try:
            with httpx.Client() as client:
                url = f"{self.base_url}/analytics/timeline"
                params = {"lab": lab} if lab else {}
                response = client.get(url, headers=self._headers(), params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
        except Exception:
            return []
    
    def get_groups(self, lab: str = "") -> list:
        """Fetch group performance for a lab (sync version).
        
        Args:
            lab: Lab identifier.
            
        Returns:
            Group data.
        """
        try:
            with httpx.Client() as client:
                url = f"{self.base_url}/analytics/groups"
                params = {"lab": lab} if lab else {}
                response = client.get(url, headers=self._headers(), params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
        except Exception:
            return []
    
    def get_top_learners(self, lab: str = "", limit: int = 5) -> list:
        """Fetch top learners (sync version).
        
        Args:
            lab: Lab identifier.
            limit: Number of top learners to return.
            
        Returns:
            Learner data.
        """
        try:
            with httpx.Client() as client:
                url = f"{self.base_url}/analytics/top-learners"
                params = {"limit": limit}
                if lab:
                    params["lab"] = lab
                response = client.get(url, headers=self._headers(), params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
        except Exception:
            return []
    
    def get_completion_rate(self, lab: str = "") -> float:
        """Fetch completion rate for a lab (sync version).
        
        Args:
            lab: Lab identifier.
            
        Returns:
            Completion rate percentage.
        """
        try:
            with httpx.Client() as client:
                url = f"{self.base_url}/analytics/completion-rate"
                params = {"lab": lab} if lab else {}
                response = client.get(url, headers=self._headers(), params=params, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                if isinstance(data, dict):
                    return data.get("rate", 0)
                return float(data) if data else 0
        except Exception:
            return 0
    
    def trigger_sync(self) -> bool:
        """Trigger ETL sync (sync version).
        
        Returns:
            True if sync triggered successfully.
        """
        try:
            with httpx.Client() as client:
                url = f"{self.base_url}/pipeline/sync"
                response = client.post(url, headers=self._headers(), timeout=self.timeout)
                response.raise_for_status()
                return True
        except Exception:
            return False
