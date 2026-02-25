from collections import deque
import logging 



#TODO: 
"""I need a persistent checkpointer to save the graph state to a database for each thread, 
and then a table for metadata of each convo (thread id, title, ..), 
when the user selects one convo, I use that thread id to start from
 the exact graph state associated to the the selected thread id 
 and stored in the checkpointer"""

logger = logging.getLogger("memory")
#later we can swap with redis, postgres or vector DB


class LongTermMemory:
    def __init__(self, max_messages: int):
        self.max_messages = max_messages
        self.store : dict[deque] = {}
        logger.info("memory initialized.")


    def load(self, session_id: str):
        logger.debug(f"called Memory.load with session id {session_id}")
        return list(self.store.get(session_id, []))
    

    def save(self, session_id: str, messages: list):
        logger.debug(f"called Memory.save with session id {session_id}")
        self.store[session_id] = deque(
            messages, maxlen=self.max_messages
        )

