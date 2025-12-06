#orchestration
from agent.agent import Agent
from config.model_config import base_url, model
from config.credentials.model_key import model_api_key


agent = Agent(base_url=base_url, model=model, api_key= model_api_key)

context = []

try: 
    while True:
        message = str(input("User: "))
        context.append({"role" : "user", "content" : message})

        response = agent.chat(prompt= context)
        print("Working...")
        print("GestAI: ", response)
        context.append({"role" : "assistant", "content": response})

except KeyboardInterrupt: 
    print("\nchat terminated.")