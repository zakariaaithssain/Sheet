from agent.runtime import AgentRuntime

import logging 


logger = logging.getLogger("interface")


def start_api(agent_runtime:AgentRuntime):
        logger.debug("called Interface.start_api")
        with agent_runtime as runtime:
            logger.debug("inside runtime context manager")
            steps = 0 
            while True:
                user_input = str(input("(q to quit)\n"))
                if user_input.strip() in "qQ":
                    logger.info("user input was 'q', breaked from loop.")
                    break
                else:
                    print()
                    runtime.step(user_input)
                    steps+=1
                    logger.debug(f"step (1-indexed): {steps}")
                    print()
