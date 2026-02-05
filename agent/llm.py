from langchain.agents import create_agent

import logging 

from config.agent_config import SYSTEM_PROMPT, TOOLS
from config.settings import MODEL_PROVIDER #env variable




class LLMClient:
    def __init__(self, model_name, temperature):
        self.model_name = model_name
        self.temperature = temperature

    def run(self, messages, tools=None):
        """
        - takes standardized messages
        - returns a string or structured output
        """
        # call provider here
        # handle retries
        # raise domain-specific errors
        return "response"


















logger = logging.getLogger("agent")


agent = create_agent(model=MODEL_PROVIDER,
                      system_prompt=SYSTEM_PROMPT,
                      tools=TOOLS
                        )

def send_prompt(messages: list[dict]): 
  reasoning = ""
  full_response = ""

  for token, _ in agent.stream(input={'messages': messages}, 
                            stream_mode="messages"): 
      
      blocks = token.content_blocks
      if not blocks:
          continue
      
      for block in blocks:
          if block["type"] == "text":
              print(block["text"], flush=True, end="")
              full_response += block["text"]

          elif block["type"] == "reasoning":
              reasoning += block["reasoning"]
  
  user_mssg = messages[-1]["prompt"] if messages[-1]["role"] == "user" else ""            
  logger.debug(f"USER: {user_mssg} REASONING: {reasoning}")

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

