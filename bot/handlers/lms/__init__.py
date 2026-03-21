"""LMS integration handlers.

These handlers fetch data from the LMS backend API.
Implements: /labs, /scores, /health with real data.
"""

import json
from typing import Optional
from bot.config import config


def handle_labs() -> str:
    """Handle /labs command - list all available labs.
    
    Returns:
        Formatted list of labs with descriptions.
    """
    try:
        import httpx
        
        # Fetch items from backend
        url = f"{config.lms_api_base_url}/items/"
        headers = {"Authorization": f"Bearer {config.lms_api_key}"}
        
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=5.0)
            response.raise_for_status()
            items = response.json()
        
        # Filter labs only
        labs = [item for item in items if item.get("type") == "lab"]
        
        if not labs:
            return "No labs available."
        
        # Format output
        result = "Available labs:\n\n"
        for lab in labs:
            title = lab.get("title", "Unknown")
            desc = lab.get("description", "")
            result += f"• {title}\n"
            if desc:
                result += f"  {desc[:60]}...\n" if len(desc) > 60 else f"  {desc}\n"
        
        return result.strip()
    
    except Exception as e:
        return f"Error fetching labs: {str(e)}"


def handle_scores(lab: Optional[str] = None) -> str:
    """Handle /scores command - show pass rates for a lab.
    
    Args:
        lab: Lab identifier (e.g., 'lab-04'). If not provided, returns instructions.
    
    Returns:
        Formatted pass rates for the lab.
    """
    if not lab:
        return "Usage: /scores lab-01\nExample: /scores lab-04"
    
    try:
        import httpx
        
        # Fetch pass rates from backend
        url = f"{config.lms_api_base_url}/analytics/pass-rates"
        headers = {"Authorization": f"Bearer {config.lms_api_key}"}
        params = {"lab": lab}
        
        with httpx.Client() as client:
            response = client.get(url, headers=headers, params=params, timeout=5.0)
            response.raise_for_status()
            pass_rates = response.json()
        
        if not pass_rates:
            return f"No data available for {lab}."
        
        # Format output
        result = f"Pass rates for {lab.upper()}:\n\n"
        for task in pass_rates:
            title = task.get("title", "Unknown task")
            avg_score = task.get("avg_score", 0)
            attempts = task.get("attempts", 0)
            
            result += f"• {title}: {avg_score}% ({attempts} attempts)\n"
        
        return result.strip()
    
    except Exception as e:
        return f"Error fetching scores for {lab}: {str(e)}"


def _get_item_count() -> int:
    """Get total count of items from backend."""
    try:
        import httpx
        
        url = f"{config.lms_api_base_url}/items/"
        headers = {"Authorization": f"Bearer {config.lms_api_key}"}
        
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=5.0)
            response.raise_for_status()
            items = response.json()
        
        return len(items)
    except Exception:
        return 0
