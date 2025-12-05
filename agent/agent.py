import json 
from openai import OpenAI

from config.model_config import system_prompt, TOOLS, FUNCTIONS

class Agent: 
    def __init__(self, base_url : str, api_key : str, model : str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model


    def chat(self, message : str):
        response = self.client.chat.completions.create(
                model = self.model, 
                messages = [{"role" : "system", "content" : system_prompt}, 
                            {"role" : "user", "content" : message}], 
                tools= TOOLS, 
                temperature = 0  #as the task is deterministic.                          
            )
        #TODO: implement tool calling flow
        pass

    
    def execute_tool_call(self, tool_call):
        """Execute a Model's tool call and return the result."""
        fn_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        
        python_fn = FUNCTIONS[fn_name]
        result = python_fn(**args)
        return result

