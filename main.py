from google.auth.exceptions import RefreshError
from agent.agent import Agent
from config.model_config import model_base_url, model_name, model_api_key

#TODO: add loggings everywhere

agent = Agent(base_url=model_base_url, model=model_name, api_key= model_api_key)

context = []

try: 
    while True:
        message = str(input("User: "))
        context.append({"role" : "user", "content" : message})

        response = agent.chat(prompt= context)
        print(f"\n{100*'-'}\nGestAI: ", response, end=f"\n{100*'-'}\n")
        context.append({"role" : "assistant", "content": response})

except KeyboardInterrupt: 
    print("\nchat terminated.")
except RefreshError: 
    print("\n The Oauth is expired, run the following script and try again: rm -rf ~/.config/gspread")