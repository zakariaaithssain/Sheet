from agent.agent import Agent
from agent.history import History
from agent.agent import Agent


import logging

logger = logging.getLogger("runtime")

class AgentRuntime:
    def __init__(self, agent: Agent, history: History, thread_id: str):
        self.agent = agent
        self.history = history
        self.thread_id = thread_id
        self.title = ""
        logger.info("runtime initialized.")



    def __enter__(self):
        logger.debug("__enter__ was called.")
    #TODO: later we should load the  old conversation corresponding to the given thread id
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("__exit__ was called.")
        self.history.save_conversation(self.thread_id, self.title)

        #to propagate exceptions normally
        return False

    def step(self, user_input: str, first_message = False):
        logger.debug("Runtime.step was called.")
        #no need for appending the messages, we now handle this using langgraph checkpointer
        if first_message: 
            self.title = self.agent.generate_convo_title(user_1st_prompt=user_input)
        
        self.agent.run_step(self.thread_id, user_input)
