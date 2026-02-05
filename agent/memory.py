from collections import deque

class InMemoryConversationStore:
    def __init__(self, max_messages: int):
        self.max_messages = max_messages
        self.store : dict[deque] = {}


    def load(self, session_id: str):
        return list(self.store.get(session_id, []))
    

    def save(self, session_id: str, messages: list):
        self.store[session_id] = deque(
            messages, maxlen=self.max_messages
        )

#later we can swap with redis, postgres or vector DB
