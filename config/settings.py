
from dataclasses import dataclass
from langchain.messages import SystemMessage

from config.tools_config import TOOLS, GOOGLE_CLIENT

import os




@dataclass(frozen=True)
class Settings:
    env : str = os.getenv("ENV", "dev")
    if env == "dev": 
        log_level: str = "DEBUG"
        handler_mode: str = "w" #to recreate logs at each run 
    else: 
        log_leve: str = "INFO"
        handler_mode: str = "a"
        
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(filename)s:%(funcName)s:%(lineno)d | %(message)s"
    log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    
    "formatters": {
        "standard": {
            "format": log_format,
        }
    },
    "handlers": {
        "agent_file": {
            "class": "logging.FileHandler",
            "filename": "logs/agent.log",
            "mode": handler_mode,
            "formatter": "standard",
            "level": log_level,
        },
        "memory_file": {
            "class": "logging.FileHandler",
            "filename": "logs/memory.log",
            "mode": handler_mode,
            "formatter": "standard",
            "level": log_level,
        },
        "runtime_file": {
            "class": "logging.FileHandler",
            "filename": "logs/runtime.log",
            "mode": handler_mode,
            "formatter": "standard",
            "level": log_level,
        },
        "tools_file": {
            "class": "logging.FileHandler",
            "filename": "logs/tools.log",
            "mode": handler_mode,
            "formatter": "standard",
            "level": log_level,
        },
        "interface_file": {
            "class": "logging.FileHandler",
            "filename": "logs/interface.log",
            "mode": handler_mode,
            "formatter": "standard",
            "level": log_level,
        },
        "main_file": {
            "class": "logging.FileHandler",
            "filename": "logs/main.log",
            "mode": handler_mode,
            "formatter": "standard",
            "level": log_level,
        },
    },

    "loggers": {
        "agent": {
            "handlers": ["agent_file"],
            "level": log_level,
            "propagate": False,
        },
        "memory": {
            "handlers": ["memory_file"],
            "level": log_level,
            "propagate": False,
        },
        "runtime": {
            "handlers": ["runtime_file"],
            "level": log_level,
            "propagate": False,
        },
        "tools": {
            "handlers": ["tools_file"],
            "level": log_level,
            "propagate": False,
        },
        "interface": {
            "handlers": ["interface_file"],
            "level": log_level,
            "propagate": False,
        },
        "main": {
            "handlers": ["main_file"],
            "level": log_level,
            "propagate": False,
        },
    },
}


    model_provider: str = os.getenv("MODEL_PROVIDER","groq:qwen/qwen3-32b" )
    max_context_messages: int = int(os.getenv("MAX_CONTEXT_MESSAGES", "30"))
    system_prompt = SystemMessage("""You are GestAI, a stateful financial assistant that manages and analyzes data in Google Sheets.
You interact with the system exclusively through the provided tools.
The tools are THE SINGLE SOURCE OF TRUTH for sheet data and metadata.
Rules:
- Act like a human assistant, you NEVER mention tools and system related terms.
- In case of errors in tool calls, suggest closest and simplest solution to the user, NEVER MENTION TOOLS NAMES.
- Suggest, but never assume defaults or infer missing parameters.
- Before performing destructive or irreversible actions, explicitly confirm with the user.
- ALWAYS use a tool call whenever the user requests data, metadata, or an action that the tools can provide.
- If the user asks about the current spTOOLSreadsheet or worksheet (name, URL, or metadata), retrieve it using the context tool.
- Do not answer questions outside sheet management or financial analysis.
- Keep responses short, direct, and action-oriented.
- Do not expose internal reasoning or implementation details.
- Do not explain internal limitations, tool calls and behavior, or system capabilities. If an action cannot be performed, state it briefly and offer a user-level alternative.
- DO NOT MENTION UNDER ANY CIRCUMSTANCES any tool names, method names, or internal function calls.
- Never explain how actions are performed internally.
- Always describe options and actions in USER-LEVEL ONLY.
- Assume data is moroccan (e.g. DHs) unless explicited. 
- Always respond in a markdown formatted user-friendly way.                                  
                                  
""")

    google_client = GOOGLE_CLIENT

    tools = TOOLS

























