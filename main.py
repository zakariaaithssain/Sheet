
from dotenv import load_dotenv
from pathlib import Path

import logging
import warnings

warnings.filterwarnings(
    "ignore",
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater",
    category=UserWarning,
)



#we should load env before importing files (calling main)
logger = logging.getLogger("main")
logger.info("loading env...")
env_path = Path(".env")
if not env_path.exists():
    raise FileNotFoundError(f".env file not found at {env_path}")
load_dotenv(dotenv_path=env_path, override=True)




def main():

    from config.settings import Settings
    from config.logging_config import setup_logging
    from agent.runtime import AgentRuntime
    from agent.memory import InMemoryConversationStore
    from agent.agent import Agent
    from interface import start_api

    import os 

    os.makedirs("logs", exist_ok = True)
    settings = Settings()
    setup_logging(settings)

    logger.info("setting memory...")
    memory = InMemoryConversationStore(settings.max_context_messages)

    logger.info("setting agent...")
    agent = Agent(
        model_provider=settings.model_provider, 
        tools=settings.tools, 
        system_prompt=settings.system_prompt
    )
    logger.info("setting runtime...")
    runtime = AgentRuntime(
        agent=agent, 
        memory=memory, 
        session_id="zakaria123"
    )
    logger.info("starting interface...")
    start_api(runtime)
    




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt: 
        logger.error("interrupted manually.")
        exit(0)
    except Exception as e: 
        logger.critical(f"unexpected exception: {e}")
        raise








