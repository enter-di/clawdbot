"""Core agentic loop — Claude tool_use cycle with n8n execution."""

import json
from typing import Any

import anthropic

from openclaw.agent.conversation import ConversationManager
from openclaw.agent.system_prompt import SYSTEM_PROMPT
from openclaw.agent.tool_registry import TOOLS
from openclaw.config import settings
from openclaw.n8n.client import invoke_tool
from openclaw.utils.logging import get_logger

logger = get_logger(__name__)


class ClaudeAgent:
    def __init__(self, conversation_manager: ConversationManager) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        self._conv = conversation_manager

    async def run(self, user_message: str, chat_id: int) -> str:
        """Process a user message and return Claude's final text response."""
        await self._conv.append(chat_id, "user", user_message)
        history = await self._conv.load(chat_id)

        for iteration in range(settings.max_agent_iterations):
            logger.info("agent_iteration", chat_id=chat_id, iteration=iteration)

            response = await self._client.messages.create(
                model=settings.claude_model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=TOOLS,  # type: ignore[arg-type]
                messages=history,
            )

            if response.stop_reason == "end_turn":
                text = next(
                    (b.text for b in response.content if hasattr(b, "text")), ""
                )
                await self._conv.append(chat_id, "assistant", response.content)
                return text

            if response.stop_reason == "tool_use":
                # Append assistant's tool_use message to history
                await self._conv.append(chat_id, "assistant", response.content)
                history = await self._conv.load(chat_id)

                # Execute each tool and collect results
                tool_results: list[dict[str, Any]] = []
                for block in response.content:
                    if block.type != "tool_use":
                        continue
                    logger.info("tool_called", tool=block.name, input=block.input)
                    try:
                        result = await invoke_tool(block.name, block.input)
                    except Exception as exc:
                        result = json.dumps({"error": str(exc)})
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )

                # Feed results back as a user message
                await self._conv.append(chat_id, "user", tool_results)
                history = await self._conv.load(chat_id)
                continue

            # Unexpected stop reason
            break

        logger.warning("max_iterations_reached", chat_id=chat_id)
        return "I reached the maximum number of steps. Please try rephrasing your request."
