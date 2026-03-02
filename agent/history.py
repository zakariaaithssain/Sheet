import logging 
import inquirer

from datetime import datetime
from rich.markdown import Markdown

from config.settings import Settings





logger = logging.getLogger("memory")

class History:
    def __init__(self):
        self.conn = Settings.postgres_connection
        self.console = Settings.console
        #setup conversations table if it doesn't exist
        CREATE_CONVERSATIONS_TABLE = """
        CREATE TABLE IF NOT EXISTS conversations (
            thread_id TEXT PRIMARY KEY,
            title TEXT NOT NULL, 
            updated_at TIMESTAMP NOT NULL
        );
        """
        with self.conn.cursor() as cursor:
            cursor.execute(CREATE_CONVERSATIONS_TABLE)

        logger.info("memory initialized.")




    def save_conversation(self, thread_id: str, title: str):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO conversations (thread_id, title, updated_at)
                VALUES (%s, %s, %s)
                ON CONFLICT (thread_id) DO UPDATE
                SET updated_at = EXCLUDED.updated_at
                """,
                (thread_id, title, datetime.now())
            )





    def _load_all_conversations(self):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT thread_id, title, updated_at 
                FROM conversations 
                ORDER BY updated_at DESC
                """
            )
            return cursor.fetchall()
        

    





    def pick_conversation(self) -> str:
        """pick an old conversation and return its thread id  
        once the thread id is given to the agent's checkpointer, it automatically 
        loads the state corresponding to that id, and resumes agent's graph from there, so no need for a 
        load conversation function"""
        
        convos_list = self._load_all_conversations()
        if convos_list: 
            choices = [
                (f"{row['title']} — last update: {row['updated_at'].strftime('%Y-%m-%d  %H:%M')}", row['thread_id'])
                for row in convos_list
            ]

            questions = [
                inquirer.List("conversation",
                    message="select a conversation",
                    choices=choices,
                )
            ]
            
            answer = inquirer.prompt(questions)
            return answer["conversation"]  # returns the thread_id
        else: 
            #empty history
            self.console.print(Markdown("*`no conversations to show`*"))
            return None