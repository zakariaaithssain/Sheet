#orchestration
from agent.agent import Agent
from config.model_config import base_url, model
from config.credentials.model_key import model_api_key


agent = Agent(base_url=base_url, model=model, api_key= model_api_key)

while True:
    prompt = str(input("User: "))
    response = agent.chat( prompt= prompt)
    print("GestAI: ", response)