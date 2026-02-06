import logging

from langchain.agents import create_agent
from langchain.messages import SystemMessage


logger = logging.getLogger("agent")


class Agent:
    def __init__(self, model_provider:str, tools:list, system_prompt: SystemMessage):
        self.model_provider = model_provider
        self.system = system_prompt     
        self.agent = create_agent(self.model_provider,
                      system_prompt=self.system,
                      tools=tools
                        )
        logger.info("agent initialized.")

    def run(self, messages: list): 
        logger.debug("called Agent.run")
        reasoning = ""
        full_response = ""

        for token, meta in self.agent.stream(input={'messages': messages}, 
                                    stream_mode="messages"): 
            blocks = token.content_blocks
            if not blocks:
                continue
            for block in blocks:
                if block.get("type") == "text":
                    print(block["text"], flush=True, end="")
                    full_response += block["text"]

                elif block["type"] == "reasoning":
                    reasoning += block["reasoning"]
        
        logging.debug(f"user prompt (trimmed): {list(messages[-1])[:30]}")
        logging.debug(f"model reasoning (trimmed): {reasoning[:30]}")
        logging.debug(f"model response (trimmed): {full_response[:30]}")

        return full_response

























#deprecated (used befor I decided to use langchain)

# import json 
# from openai import OpenAI

# from config.model_config import SYSTEM_PROMPT, FUNCTIONS_DEF, FUNCTIONS_MAP



# class Agent: 
#     def __init__(self, base_url : str, api_key : str, model : str):
#         self.client = OpenAI(base_url=base_url, api_key=api_key)
#         self.model = model
        


#     def chat(self, prompt : list[dict]):
#         context = [{"role" : "system", "content" : SYSTEM_PROMPT}]
#         context += prompt
#         while True:
#             response = self.client.chat.completions.create(
#                     model = self.model, 
#                     messages = context, 
#                     functions = FUNCTIONS_DEF, 
#                     temperature = 0  #as the task is deterministic.                          
#                 )
            
#             msg = response.choices[0].message
#             context.append(msg)

#             function_calls = msg.tool_calls
#             if function_calls: 
#                 for call in function_calls:
#                     if call.type == 'function':
#                         result = self.execute_fn_call(call)
#                         #add function calls results to 'context' 
#                         context.append({
#                                 "role": "function",
#                                 "name": call.function.name,
#                                 "content": json.dumps(result)})
#                 continue
#             else: 
#                 return msg.content
            
                
                
        


    
#     def execute_fn_call(self, fn_call):
#         """Execute a Model's function call and return the result."""
#         #this parsing is based on the structure of the model's return (ChatCompletionMessageToolCallUnion)
#         fn_name = fn_call.function.name
#         args = json.loads(fn_call.function.arguments)
        
#         python_fn = FUNCTIONS_MAP[fn_name]
#         result = python_fn(**args)
#         return result

