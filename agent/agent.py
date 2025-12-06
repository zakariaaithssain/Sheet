import json 
from openai import OpenAI

from config.model_config import system_prompt, FUNCTIONS_DEF, FUNCTIONS_MAP

class Agent: 
    def __init__(self, base_url : str, api_key : str, model : str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model


    def chat(self, message : str):
        response = self.client.chat.completions.create(
                model = self.model, 
                messages = [{"role" : "system", "content" : system_prompt}, 
                            {"role" : "user", "content" : message}], 
                functions = FUNCTIONS_DEF, 
                temperature = 0  #as the task is deterministic.                          
            )
        #TODO: implement tool calling flow
        calls = response.choices[0].message.tool_calls
        results = []
        for call in calls:
            if call.type == 'function':
                result = self.execute_fn_call(call)
                results.append(result)
        return results
    


    
    def execute_fn_call(self, fn_call):
        """Execute a Model's function call and return the result."""
        #this parsing is based on the structure of the model's return (ChatCompletionMessageToolCallUnion)
        fn_name = fn_call.function.name
        args = json.loads(fn_call.function.arguments)
        
        python_fn = FUNCTIONS_MAP[fn_name]
        result = python_fn(**args)
        return result

