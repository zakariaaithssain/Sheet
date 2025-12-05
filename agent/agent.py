from openai import OpenAI

from config.model_config import system_prompt


class Agent: 
    def __init__(self, base_url : str, api_key : str, model : str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model


    def chat(self, message : str):
        responses = self.client.chat.completions.create(
                model = self.model, 
                messages = [{"role" : "system", "content" : system_prompt}, 
                            {"role" : "user", "content" : message}], 
                temperature = 0  #as the task is deterministic.                          
            )
        return responses.choices[0].message["content"]

