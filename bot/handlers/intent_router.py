"""Intent-based natural language router using LLM with tool calling.

Routes user messages to appropriate data fetching based on intent.
Uses LLM to understand user query and call backend APIs as needed.
"""

import sys
import json
from typing import Optional
from bot.config import config
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
        system_prompt = """You are a helpful LMS assistant. Users ask questions about labs, scores, and performance.
You have access to tools that fetch real data from the LMS backend.

When a user asks a question:
1. Decide which tool(s) you need to call to answer their question.
2. Call the appropriate tool with the right parameters.
3. When you receive tool results, analyze them and provide a helpful answer.

For multi-step queries (e.g., "which lab has the lowest pass rate?"):
1. Call get_items to find all labs
2. Call get_pass_rates for each lab
3. Compare the results and give a clear answer with specific numbers

Always provide specific data when possible - include percentages, names, numbers.
If you don't have enough data to answer, say so clearly."""
        
        # Initialize conversation
        messages = [
            {"role": "user", "content": user_message}
        ]
        
        # Tool calling loop
        max_iterations = 10
        iteration = 0
        tool_results_count = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Call LLM
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
            
            # Execute tool calls
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
                tool_results_count += 1
            
            # Append tool results to messages for LLM context
            if tool_results:
                tool_result_text = "\n".join([
                    f"Tool '{tr['tool']}' with args {tr['arguments']}: {tr['result']}"
                    for tr in tool_results
                ])
                
                messages.append({"role": "assistant", "content": response_text or ""})
                messages.append({
                    "role": "user",
                    "content": f"Here are the tool results:\n{tool_result_text}\n\nNow provide a final answer based on this data."
                })
                
                print(f"[summary] Feeding {len(tool_results)} tool results back to LLM", file=sys.stderr)
            else:
                # No more tools to call, return response
                return response_text if response_text else "I couldn't find the information you're looking for."
        
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
        Formatted result string.
    """
    try:
        if tool_name == "get_items":
            items = lms.get_items()
            labs = [i for i in items if i.get("type") == "lab"]
            return f"{len(items)} total items, {len(labs)} labs"
        
        elif tool_name == "get_learners":
            learners = lms.get_learners()
            return f"{len(learners)} learners enrolled"
        
        elif tool_name == "get_scores":
            lab = tool_args.get("lab", "")
            if lab:
                data = lms.get_scores(lab=lab)
            else:
                data = lms.get_scores()
            return json.dumps(data)[:200]
        
        elif tool_name == "get_pass_rates":
            lab = tool_args.get("lab", "")
            if lab:
                data = lms.get_pass_rates(lab=lab)
                if isinstance(data, list) and data:
                    avg_score = sum(d.get("avg_score", 0) for d in data) / len(data)
                    return f"Lab {lab}: {len(data)} tasks, avg score {avg_score:.1f}%"
                return f"Lab {lab}: no data"
            return "Lab parameter required"
        
        elif tool_name == "get_timeline":
            lab = tool_args.get("lab", "")
            if lab:
                data = lms.get_timeline(lab=lab)
                return f"Timeline for {lab}: {len(data) if isinstance(data, list) else 'no'} data points"
            return "Lab parameter required"
        
        elif tool_name == "get_groups":
            lab = tool_args.get("lab", "")
            if lab:
                data = lms.get_groups(lab=lab)
                return f"Groups in {lab}: {len(data) if isinstance(data, list) else 'no'} groups"
            return "Lab parameter required"
        
        elif tool_name == "get_top_learners":
            limit = tool_args.get("limit", 5)
            lab = tool_args.get("lab", "")
            if lab:
                data = lms.get_top_learners(lab=lab, limit=limit)
            else:
                data = lms.get_top_learners(limit=limit)
            return f"Top {limit} learners: {len(data) if isinstance(data, list) else 'no'} results"
        
        elif tool_name == "get_completion_rate":
            lab = tool_args.get("lab", "")
            if lab:
                data = lms.get_completion_rate(lab=lab)
                return f"Completion rate for {lab}: {data if isinstance(data, (int, float)) else 'unknown'}%"
            return "Lab parameter required"
        
        elif tool_name == "trigger_sync":
            result = lms.trigger_sync()
            return "Sync triggered successfully" if result else "Sync failed"
        
        else:
            return f"Unknown tool: {tool_name}"
    
    except Exception as e:
        return f"Error executing {tool_name}: {str(e)}"


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
