#orchestration
from agent.agent import Agent
from config.model_config import base_url, model
from config.credentials.model_key import model_api_key


agent = Agent(base_url=base_url, model=model, api_key= model_api_key)

results = agent.chat("create a sheet named 'created_by_model' that has columns: 'a', 'b' and 'c'")
print("resulted calls: ")
for result in results: 
    print(result) 