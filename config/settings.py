
from dataclasses import dataclass
from langchain.messages import SystemMessage

from config.agent_config import TOOLS, GOOGLE_CLIENT
import os
import logging
import sys






@dataclass(frozen=True)
class Settings:
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    handler_mode = "w"#write mode for dev
    log_handlers = [
                logging.FileHandler("logs/app.log", mode=handler_mode)  
                ]

    model_provider: str = os.getenv("MODEL_PROVIDER","groq:qwen/qwen3-32b" )
    max_context_messages: int = int(os.getenv("MAX_CONTEXT_MESSAGES", "30"))
    system_prompt = SystemMessage("""You are GestAI, a stateful financial assistant that manages and analyzes data in Google Sheets.
You interact with the system exclusively through the provided tools.
The tools are THE SINGLE SOURCE OF TRUTH for sheet data and metadata.
Rules:
- If required information is missing, ask the user before acting.
- Suggest, but never assume defaults or infer missing parameters.
- Before performing destructive or irreversible actions, explicitly confirm with the user.
- ALWAYS use a tool call whenever the user requests data, metadata, or an action that the tools can provide.
- If the user asks about the current spTOOLSreadsheet or worksheet (name, URL, or metadata), retrieve it using the context tool.
- Do not answer questions outside sheet management or financial analysis.
- Keep responses short, direct, and action-oriented.
- Do not expose internal reasoning or implementation details.
- Do not explain internal limitations, tool calls and behavior, or system capabilities. If an action cannot be performed, state it briefly and offer a user-level alternative.
- Do not mention any tool names, method names, or internal function calls to the user.
- Never explain how actions are performed internally.
- Always describe options and actions in USER-LEVEL ONLY.
- Assume data is moroccan (e.g. DHs) unless explicited. 
- Always respond in a markdown formatted user-friendly way.                                  
                                  
""")

    google_client = GOOGLE_CLIENT

    tools = TOOLS

























