import logging 

from datetime import datetime
from config.settings import Settings

#TODO: FIX HISTORY ITS NOT WORKING PROPERLY, check also interface.py
#NOTE: DO NOT USE f-strings for queries, that causes SQL injection
#TODO: 
"""I need a persistent checkpointer to save the graph state to a database for each thread, 
and then a table for metadata of each convo (thread id, title, ..), 
when the user selects one convo, I use that thread id to start from
 the exact graph state associated to the the selected thread id 
 and stored in the checkpointer"""

logger = logging.getLogger("memory")
#later we can swap with redis, postgres or vector DB


class History:
    def __init__(self):
        self.conn = Settings.postgres_connection

        #setup conversations table if it doesn't exist
        CREATE_CONVERSATIONS_TABLE = """
        CREATE TABLE IF NOT EXISTS conversations (
            thread_id TEXT PRIMARY KEY,
            title TEXT NOT NULL, 
            created_at TIMESTAMP NOT NULL
        );
        """
        with self.conn.cursor() as cursor:
            cursor.execute(CREATE_CONVERSATIONS_TABLE)

        logger.info("memory initialized.")



    def save_conversation(self, thread_id: str, title: str):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO conversations (thread_id, title, created_at)
                VALUES (%s, %s, %s)
                ON CONFLICT (thread_id) DO NOTHING
                """,
                (thread_id, title, datetime.now())
            )

    def load_conversations(self):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT thread_id, title, created_at 
                FROM conversations 
                ORDER BY created_at DESC
                """
            )
            yield from cursor   # cursor is still open while generator is alive

    def load_conversation(self, thread_id: str):
        with self.conn.cursor() as cursor:
            results = cursor.execute(
                "SELECT thread_id, title, created_at FROM conversations WHERE thread_id = %s",
                (thread_id,)
            )
            return results.fetchone()