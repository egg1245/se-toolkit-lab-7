"""Intent-based natural language router using LLM with tool calling.

Routes user messages to appropriate data fetching based on intent.
Uses LLM to understand user query and call backend APIs as needed.
"""

import sys
import json
from typing import Optional
from bot.config import get_config
from bot.services.llm_client import LLMClient
from bot.services.lms_client import LMSClient


def route_intent(user_message: str) -> str:
    """Route user message through LLM intent router with tool calling.
    
    Args:
        user_message: User's natural language message.
        
    Returns:
        Bot response based on LLM reasoning and API data.
    """
    try:
        # Get config
        config = get_config()
        
        # Initialize clients
        llm = LLMClient(
            api_base_url=config.llm_api_base_url,
            api_key=config.llm_api_key,
        )
        lms = LMSClient(
            base_url=config.lms_api_base_url,
            api_key=config.lms_api_key,
        )
        
        # Define available tools
        tools = define_tools()
        
        # System prompt for tool calling
        system_prompt = """You are a helpful LMS assistant. Answer questions about labs, students, and performance.
Your tools give you real data from the LMS backend. Use them to answer questions accurately.

When user asks about labs, students, or performance:
- Use get_items to list all labs and courses
- Use get_learners to count enrolled students
- Use get_pass_rates, get_scores to get actual performance numbers
- Use get_timeline, get_groups, get_top_learners for detailed analysis
- Always include specific numbers, percentages, lab names in your answer

Example: User asks "what labs are available?"
- Call get_items
- Return list with lab names like "Lab 01 — ...", "Lab 02 — ...", etc.

Example: User asks "how many students are enrolled?"  
- Call get_learners
- Return the count of learners, e.g., "42 students enrolled"

Always provide real data from the tools, not generic answers."""
        
        # Initialize conversation
        messages = [
            {"role": "user", "content": user_message}
        ]
        
        # Tool calling loop
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Call LLM with full context
            response = llm.ask(user_message, tools, system_prompt, messages)
            
            # Parse response
            if isinstance(response, dict):
                response_text = response.get("message", "")
                tool_calls = response.get("tool_calls", [])
            else:
                # Assume string response - no tool calls
                return response
            
            # If no tool calls, return the response
            if not tool_calls:
                return response_text if response_text else "I don't have enough information to answer that."
            
            # Execute tool calls and collect results
            tool_results = []
            for tool_call in tool_calls:
                tool_name = tool_call.get("name", "")
                tool_args = tool_call.get("arguments", {})
                
                print(f"[tool] LLM called: {tool_name}({tool_args})", file=sys.stderr)
                
                result = execute_tool(lms, tool_name, tool_args)
                
                print(f"[tool] Result: {result}", file=sys.stderr)
                
                tool_results.append({
                    "tool": tool_name,
                    "arguments": tool_args,
                    "result": result,
                })
            
            # If no tools were actually executed, return response
            if not tool_results:
                return response_text if response_text else "I couldn't process that request."
            
            # Append to conversation: assistant response and tool results
            messages.append({"role": "assistant", "content": response_text or ""})
            
            # Create tool results message
            tool_result_text = "\n".join([
                f"{tr['tool']}: {tr['result']}"
                for tr in tool_results
            ])
            
            messages.append({
                "role": "user",
                "content": f"Tool results:\n{tool_result_text}\n\nProvide final answer with specific data from these results."
            })
            
            print(f"[summary] Feeding {len(tool_results)} tool results back to LLM", file=sys.stderr)
        
        return "I reached the maximum number of tool calls. Please try a simpler question."
    
    except Exception as e:
        return f"Error processing your request: {str(e)}"


def execute_tool(lms: LMSClient, tool_name: str, tool_args: dict) -> str:
    """Execute a backend tool and return formatted result.
    
    Args:
        lms: LMS client instance.
        tool_name: Name of tool to execute.
        tool_args: Arguments for the tool.
        
    Returns:
        Formatted result string with real backend data.
    """
    try:
        if tool_name == "get_items":
            items = lms.get_items()
            if not items:
                return "No items found"
            
            # Format: list items with titles
            result_lines = [f"{len(items)} items total:"]
            for item in items[:10]:  # Limit to 10 for readability
                title = item.get("title", "Unknown")
                item_type = item.get("type", "")
                result_lines.append(f"- {title} ({item_type})")
            return "\n".join(result_lines)
        
        elif tool_name == "get_learners":
            learners = lms.get_learners()
            if not learners:
                return "No learners found"
            count = len(learners)
            # Include actual numbers
            return f"{count} students enrolled"
        
        elif tool_name == "get_scores":
            lab = tool_args.get("lab", "")
            data = lms.get_scores(lab=lab) if lab else lms.get_scores()
            if not data:
                return f"No score data for {lab or 'all labs'}"
            # Return JSON string of actual data
            return json.dumps(data)[:500]
        
        elif tool_name == "get_pass_rates":
            lab = tool_args.get("lab", "")
            if not lab:
                return "Lab parameter required for get_pass_rates"
            
            data = lms.get_pass_rates(lab=lab)
            if not data:
                return f"No pass rate data for {lab}"
            
            # Format with actual percentages and task names
            if isinstance(data, list) and data:
                result_lines = [f"Pass rates for {lab}:"]
                avg_total = 0
                for item in data:
                    task_name = item.get("name", "Task")
                    avg_score = item.get("avg_score", 0)
                    attempts = item.get("attempts", 0)
                    result_lines.append(f"  {task_name}: {avg_score:.1f}% ({attempts} attempts)")
                    avg_total += avg_score
                
                if data:
                    avg_total /= len(data)
                    result_lines.append(f"Average: {avg_total:.1f}%")
                return "\n".join(result_lines)
            return f"No detailed pass rate data for {lab}"
        
        elif tool_name == "get_timeline":
            lab = tool_args.get("lab", "")
            if not lab:
                return "Lab parameter required for get_timeline"
            
            data = lms.get_timeline(lab=lab)
            if not data:
                return f"No timeline data for {lab}"
            
            if isinstance(data, list):
                return f"Timeline for {lab}: {len(data)} submissions recorded"
            return json.dumps(data)[:300]
        
        elif tool_name == "get_groups":
            lab = tool_args.get("lab", "")
            if not lab:
                return "Lab parameter required for get_groups"
            
            data = lms.get_groups(lab=lab)
            if not data:
                return f"No group data for {lab}"
            
            if isinstance(data, list) and data:
                result_lines = [f"Group performance for {lab}:"]
                for item in data:
                    group_name = item.get("name", "Group")
                    score = item.get("avg_score", 0)
                    count = item.get("count", 0)
                    result_lines.append(f"  {group_name}: {score:.1f}% ({count} students)")
                return "\n".join(result_lines)
            return json.dumps(data)[:300]
        
        elif tool_name == "get_top_learners":
            limit = tool_args.get("limit", 5)
            lab = tool_args.get("lab", "")
            
            data = lms.get_top_learners(lab=lab, limit=limit) if lab else lms.get_top_learners(limit=limit)
            
            if not data:
                return f"No learner data found"
            
            if isinstance(data, list):
                scope = f"in {lab}" if lab else "overall"
                result_lines = [f"Top {limit} learners {scope}:"]
                for i, item in enumerate(data[:limit], 1):
                    name = item.get("name", "Unknown")
                    score = item.get("score", 0)
                    result_lines.append(f"  {i}. {name}: {score:.1f}%")
                return "\n".join(result_lines)
            return json.dumps(data)[:300]
        
        elif tool_name == "get_completion_rate":
            lab = tool_args.get("lab", "")
            if not lab:
                return "Lab parameter required for get_completion_rate"
            
            rate = lms.get_completion_rate(lab=lab)
            return f"Completion rate for {lab}: {rate:.1f}%"
        
        elif tool_name == "trigger_sync":
            result = lms.trigger_sync()
            return "Data sync triggered successfully" if result else "Failed to trigger sync"
        
        else:
            return f"Unknown tool: {tool_name}"
    
    except Exception as e:
        return f"Error calling {tool_name}: {str(e)}"


def define_tools() -> list[dict]:
    """Define all 9 backend tools for LLM.
    
    Returns:
        List of tool definitions in OpenAI format.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "get_items",
                "description": "Get list of all labs, tasks, courses, and assignments. Returns titles, descriptions, types, and metadata.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_learners",
                "description": "Get list of enrolled students and learners with their groups and enrollment status.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_scores",
                "description": "Get score distribution for a lab (4 buckets: low/medium-low/medium-high/high). Shows how many students fall into each score range.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lab": {"type": "string", "description": "Lab identifier, e.g., 'lab-01'"},
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_pass_rates",
                "description": "Get per-task average scores and attempt counts for a lab. Shows what percentage of students passed each task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lab": {"type": "string", "description": "Lab identifier, e.g., 'lab-01' or 'lab-04'"},
                    },
                    "required": ["lab"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_timeline",
                "description": "Get submission timeline for a lab - shows when students submitted work (submissions per day).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lab": {"type": "string", "description": "Lab identifier, e.g., 'lab-01'"},
                    },
                    "required": ["lab"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_groups",
                "description": "Get per-group performance metrics for a lab. Shows how each student group (A, B, C, etc) is performing and their average scores.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lab": {"type": "string", "description": "Lab identifier, e.g., 'lab-01'"},
                    },
                    "required": ["lab"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_top_learners",
                "description": "Get top N learners by score for a lab or overall. Shows the highest-performing students.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lab": {"type": "string", "description": "Lab identifier, e.g., 'lab-01'. If omitted, returns overall top learners."},
                        "limit": {"type": "integer", "description": "How many top learners to return. Default is 5."},
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_completion_rate",
                "description": "Get the percentage of students who completed a lab or assignment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lab": {"type": "string", "description": "Lab identifier, e.g., 'lab-01'"},
                    },
                    "required": ["lab"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "trigger_sync",
                "description": "Trigger ETL data sync from the autochecker to update all grades and submissions in the LMS.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
    ]
