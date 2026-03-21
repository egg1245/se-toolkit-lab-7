"""LLM client for task-3 with tool calling support.

Communicates with LLM service for intent routing.
Tools are described formally; LLM receives descriptions and decides which to invoke.

Pattern: Function calling / Tool use.
- Tools have formal descriptions (name, description, parameters).
- LLM receives descriptions and user query.
- LLM chooses which tool(s) to call.
- System executes tool and returns result.

IMPORTANT: This client does NOT use regex or keyword matching for routing.
Tool selection is based on tool descriptions - if LLM isn't calling the right tool,
improve the descriptions, not the code routing.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class ToolDefinition:
    """Description of a tool that LLM can invoke.
    
    Attributes:
        name: Tool identifier (e.g., "get_labs").
        description: Human-readable description of what tool does.
        input_schema: JSON schema describing parameters.
    """

    name: str
    description: str
    input_schema: dict[str, Any]


class LLMClient:
    """LLM client for intent routing and tool calling.
    
    In production, this would communicate with a real LLM service (OpenAI, Anthropic, etc).
    For testing and MVP, this is a mock that demonstrates the tool calling interface.
    """

    def __init__(self, api_base_url: str, api_key: str):
        """Initialize LLM client.
        
        Args:
            api_base_url: Base URL of LLM service.
            api_key: API key for authentication.
        """
        self.api_base_url = api_base_url
        self.api_key = api_key

    def define_tools(self) -> list[ToolDefinition]:
        """Define tools available to LLM.
        
        Tool descriptions are the key to good LLM routing.
        LLM reads these descriptions and decides which tool to call.
        
        Returns:
            List of tool definitions.
        """
        return [
            ToolDefinition(
                name="get_labs",
                description=(
                    "Retrieves a list of available labs, assignments, and courses from the LMS. "
                    "Each lab contains metadata: title, description, due date, and submission status. "
                    "Use this when the user asks about: 'What labs are available?', 'Show me assignments', "
                    "'List my courses', 'What do I need to submit?', 'What assignments are pending?'"
                ),
                input_schema={
                    "type": "object",
                    "properties": {
                        "filter": {
                            "type": "string",
                            "description": "Optional filter: 'active', 'completed', or 'all'. Defaults to 'active'.",
                        }
                    },
                    "required": [],
                },
            ),
            ToolDefinition(
                name="get_scores",
                description=(
                    "Retrieves the current user's scores, grades, and performance metrics from the LMS. "
                    "Returns overall GPA, individual assignment scores, and progress statistics. "
                    "Use this when the user asks about: 'What are my grades?', 'Show my scores', "
                    "'How am I doing?', 'What is my GPA?', 'Show my performance'"
                ),
                input_schema={
                    "type": "object",
                    "properties": {
                        "period": {
                            "type": "string",
                            "description": "Optional period filter: 'current', 'semester', 'all'. Defaults to 'current'.",
                        }
                    },
                    "required": [],
                },
            ),
        ]

    async def ask_llm(self, prompt: str, tools: list[ToolDefinition] | None = None) -> dict[str, Any]:
        """Ask LLM to process prompt and choose tool (mock implementation).
        
        In production, this would:
        1. Send prompt + tool descriptions to LLM API
        2. Get back tool choice and parameters
        3. Execute tool and stream result back
        
        For now, this is a mock that demonstrates the interface.
        
        Args:
            prompt: User question/prompt.
            tools: Available tools (if None, uses define_tools()).
            
        Returns:
            Dict with:
            - "tool": name of chosen tool (or None if no tool needed)
            - "params": parameters for tool call
            - "reasoning": why tool was chosen
        """
        if tools is None:
            tools = self.define_tools()

        # Mock implementation: In production, send to real LLM service
        # For now, return a placeholder indicating tool calling would happen
        return {
            "tool": None,
            "params": {},
            "reasoning": "Tool calling not implemented yet. In production, LLM would read tool descriptions and choose.",
            "available_tools": [{"name": t.name, "description": t.description} for t in tools],
        }
