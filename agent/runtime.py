from agent.agent import Agent
from agent.memory import InMemoryConversationStore
from langchain.messages import HumanMessage, AIMessage
from agent.agent import Agent
from langchain.messages import HumanMessage, AIMessage
import logging

logger = logging.getLogger("runtime")

class AgentRuntime:
    def __init__(self,
        agent: Agent,
        memory: InMemoryConversationStore,
        session_id: str,
    ):
        self.agent = agent
        self.memory = memory
        self.session_id = session_id
        self.messages = None
        logger.info("runtime initialized.")



    def __enter__(self):
        logger.debug("__enter__ was called.")
        self.messages = self.memory.load(self.session_id)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("__exit__ was called.")
        self.memory.save(self.session_id, self.messages)

        #to propagate exceptions normally
        return False

    def step(self, user_input: str):
        logger.debug("Runtime.step was called.")
        self.messages.append(HumanMessage(content=user_input))

        response = self.agent.run(self.messages)

        self.messages.append(AIMessage(content=response))