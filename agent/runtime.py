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

    def step(self, user_input: str, first_message = False, thread_id = None):
        logger.debug("Runtime.step was called.")
        if first_message: 
            self.title = self.agent.generate_convo_title(user_1st_prompt=user_input)
        
        #use the given id (one of an old convo) sinon use the new one given by main (new convo case)
        session_id = thread_id if thread_id else self.thread_id
        self.agent.run_step(session_id, user_input)
