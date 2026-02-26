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
            console.print(Markdown("*What did you spend today?* "))
            logger.debug("inside runtime context manager")
            history_gen = None
            steps = 0 
            while True:
                user_input = ""
                while user_input == "": 
                    user_input = str(console.input())

                console.print()
                if user_input.lower().strip() == "q":
                    logger.info("user input was 'q', breaked from loop.")
                    break
                elif user_input.lower().strip() == "h": 
                    if history_gen is None: 
                         history_gen = runtime.history.load_conversations()
                    try:
                        console.print(Markdown("*history:* "))
                        row = next(history_gen)
                        console.print(f"{row['title']} - {row['created_at']}")
                    except StopIteration:
                        console.print("No more conversations.")
                        history_gen = None  # reset so next h starts over

                else:
                    #generate the title if first message
                    if steps == 0: 
                        runtime.step(user_input, first_message=True)
                    else: 
                         runtime.step(user_input)

                    steps+=1
                    logger.debug(f"step (1-indexed): {steps}")
                    console.print()
