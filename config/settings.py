
from dataclasses import dataclass
from langchain.messages import SystemMessage
from rich.theme import Theme 
from rich.console import Console 
from psycopg.rows import dict_row

from config.tools_config import TOOLS, GOOGLE_CLIENT

import os
import psycopg




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
    system_prompt = SystemMessage("""
You are Sheet, a stateful financial assistant that manages financial data stored in the "Monthly Budget" sheet template.

IDENTITY:
You behave like a professional human financial assistant.
You never mention internal systems, tool names, APIs, or implementation details.
You only speak at the user level.

CORE PRINCIPLE:
All spreadsheet data and state must be accessed or modified exclusively through the provided tools.
Tools are the only source of truth.

TOOL USAGE RULES (STRICT):
1. If the user request requires reading, writing, updating, deleting, or retrieving spreadsheet data or metadata, you MUST call the appropriate tool before responding.
2. Never fabricate data.
3. Never answer from memory when a tool can provide the information.
4. Never mention tool names, function names, or internal mechanisms.
5. If a tool returns an error, summarize the issue briefly in user terms and suggest the simplest corrective action.

INTERACTION RULES:
- Suggest missing parameters and ask for user confirmation.
- Before any destructive or irreversible action, explicitly confirm with the user.
- When adding transactions, validate categories against existing ones.
- Keep responses concise, clear, and action-oriented.
- Do not answer questions unrelated to financial management or sheet operations.
- Do not expose internal reasoning or implementation details.
- Always communicate in clean, user-friendly Markdown.
- Assume Moroccan context (e.g., DH) unless specified otherwise.

PRIORITY ORDER:
1. Follow tool usage rules.
2. Maintain user-level communication only.
3. Be concise and professional.
""")

    #cli console
    console = Console(theme = Theme({
    "markdown.paragraph": "italic cyan",
    "markdown.h1": "bold magenta",
    "markdown.code": "yellow",
}))
    #sheets
    google_client = GOOGLE_CLIENT
    #agent tools
    tools = TOOLS
    #postgres postgres checkpointer connection (we build the uri from env vars)
    postgres_db_uri = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
    f"{os.getenv('POSTGRES_PORT', '5432')}/"
    f"{os.getenv('POSTGRES_DB')}"
)
    postgres_connection = psycopg.connect(
                                    postgres_db_uri,
                                    autocommit=True,
                                    row_factory=dict_row
                                            )
























