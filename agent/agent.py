import json 
from openai import OpenAI

from config.model_config import system_prompt, FUNCTIONS_DEF, FUNCTIONS_MAP

class Agent: 
    def __init__(self, base_url : str, api_key : str, model : str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        


    def chat(self, prompt : list[dict]):
        context = [{"role" : "system", "content" : system_prompt}]
        context += prompt
        while True:
            response = self.client.chat.completions.create(
                    model = self.model, 
                    messages = context, 
                    functions = FUNCTIONS_DEF, 
                    temperature = 0  #as the task is deterministic.                          
                )
            
            msg = response.choices[0].message
            context.append(msg)

            function_calls = msg.tool_calls
            if function_calls: 
                for call in function_calls:
                    if call.type == 'function':
                        result = self.execute_fn_call(call)
                        #add function calls results to 'context' 
                        context.append({
                                "role": "function",
                                "name": call.function.name,
                                "content": json.dumps(result)})
                continue
            else: 
                return msg.content
            
                
                
        


    
    def execute_fn_call(self, fn_call):
        """Execute a Model's function call and return the result."""
        #this parsing is based on the structure of the model's return (ChatCompletionMessageToolCallUnion)
        fn_name = fn_call.function.name
        args = json.loads(fn_call.function.arguments)
        
        python_fn = FUNCTIONS_MAP[fn_name]
        result = python_fn(**args)
        return result

