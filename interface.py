from rich.markdown import Markdown

from agent.runtime import AgentRuntime
from config.settings import Settings

import logging 


logger = logging.getLogger("interface")
console = Settings.console
console.set_window_title("Sheet, THE SHEETS AGENT")

def start_api(agent_runtime:AgentRuntime):
        logger.debug("called Interface.start_api")
        with agent_runtime as runtime:
            logger.debug("inside runtime context manager")
            steps = 0 
            while True:
                user_input = str(console.input(Markdown("*(q to quit):* ")))
                console.print()
                if user_input.strip() in "qQ":
                    console.print(Markdown("**Sheet:** See you!"))
                    logger.info("user input was 'q', breaked from loop.")
                    break
                else:
                    runtime.step(user_input)
                    steps+=1
                    logger.debug(f"step (1-indexed): {steps}")
                    console.print()
