from dotenv import load_dotenv
import logging

from agent.agent import send_prompt
from config.settings import LOG_FORMAT, LOG_HANDLERS, LOG_LEVEL


load_dotenv()

logging.basicConfig(format=LOG_FORMAT,
                    handlers=LOG_HANDLERS, 
                    level=LOG_LEVEL)


logger = logging.getLogger("main")
logger.info("starting the app")

send_prompt("what is today's date? ")



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