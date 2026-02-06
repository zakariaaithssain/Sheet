from dotenv import load_dotenv
from config.settings import Settings
from config.logging_config import setup_logging
from agent.runtime import AgentRuntime
from agent.memory import InMemoryConversationStore
from agent.agent import Agent
from interface import start_api

import os 
import logging
import google.auth.exceptions




def main():
    logger.info("loading env...")
    load_dotenv()
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
    logger = logging.getLogger("main")
    try:
        main()
    except KeyboardInterrupt: 
        logger.error("interrupted manually.")
        exit(0)
    except google.auth.exceptions.RefreshError:
        logger.error("Oauth token expired. see README on how to fix it.")
        raise
    except Exception as e: 
        logger.critical(f"unexpected exception: {e}")
        raise








