from dotenv import load_dotenv
import logging

from agent.llm import send_prompt
from config.settings import LOG_FORMAT, LOG_HANDLERS, LOG_LEVEL





from dotenv import load_dotenv
from config.settings import Settings
from config.logging_config import setup_logging
from agent.runtime import AgentRuntime
from agent.memory import InMemoryConversationStore
from agent.llm import LLMClient
from agent.tools import ToolRegistry
from interface import start_api

def main():
    load_dotenv()

    settings = Settings()
    setup_logging(settings)

    memory = InMemoryConversationStore(settings.max_context_messages)
    llm = LLMClient(settings.model_name, settings.temperature)
    tools = ToolRegistry()

    agent = AgentRuntime(llm, memory, tools)

    start_api(settings)

if __name__ == "__main__":
    main()












load_dotenv()

logging.basicConfig(format=LOG_FORMAT,
                    handlers=LOG_HANDLERS, 
                    level=LOG_LEVEL)


logger = logging.getLogger("main")
logger.info("starting the app")

prompt = []


while True:
    print("\n\n-------------------------------")
    question = input("Ask anything! (q to quit): ")
    if question == "q":
        break
    print("\n\n-------------------------------")
    #this function streams response and also returns the full response at the end
    prompt.append({"role": "user", "prompt": question})
    full_resp = send_prompt(prompt)
    prompt.append({"role": "assistant", "prompt": full_resp})
   
    



#DEPRECATED (I SWITCHED TO LANGCHAIN THAT WOULD HANDLE ALL THIS FOR ME)

# from google.auth.exceptions import RefreshError
# from agent.agent import Agent
# from config.model_config import model_base_url, model_name, model_api_key



# agent = Agent(base_url=model_base_url, model=model_name, api_key= model_api_key)

# context = []

# try: 
#     while True:
#         message = str(input("User: "))
#         print(f"{100*'-'}")
#         context.append({"role" : "user", "content" : message})
#         full_response = ""

#         #stream
#         print("GestAI: ",end="")
#         for chunk in agent.chat(prompt= context):
#             print(chunk, end="", flush=True)
#             full_response += chunk

#         print(f"\n{100*'-'}")
#         context.append({"role" : "assistant", "content": full_response})

# except KeyboardInterrupt: 
#     print("\nchat terminated.")
# except RefreshError: 
#     print("\n The Oauth is expired, run the following script and try again: rm -rf ~/.config/gspread")