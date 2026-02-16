import logging

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.messages import SystemMessage, AIMessage
from rich.markdown import Markdown

from config.settings import Settings

logger = logging.getLogger("agent")
console = Settings.console

class Agent:
    def __init__(self, model_provider:str, tools:list, system_prompt: SystemMessage):
        self.model_provider = model_provider
        self.system = system_prompt     
        self.agent = create_agent(self.model_provider,
                      system_prompt=self.system,
                      tools=tools,
                      middleware=[
                          SummarizationMiddleware(model=self.model_provider, 
                                                  trigger = ("fraction", 0.5)
                                                  )
                                ]
                        )
        logger.info("agent initialized.")

    def run(self, messages: list): 
        logger.debug("called Agent.run")
        full_response = ""

        for chunk in self.agent.stream({"messages":messages}, stream_mode="values"):         
            #each chunk contains the full state at that point
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                if isinstance(latest_message, AIMessage):
                    console.print(Markdown(f"**GestAI**: {latest_message.content}", hyperlinks=False), end='')
                    full_response += latest_message.content

            elif latest_message.tool_calls:
                console.print(Markdown("*calling tools...*"))

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

