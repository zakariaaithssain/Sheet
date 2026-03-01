import logging
import re
import json

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware
from langchain.messages import SystemMessage, AIMessageChunk, ToolMessage
from langchain.chat_models import init_chat_model

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import Command

from rich.markdown import Markdown
from rich.live import Live
from rich.panel import Panel
from rich import box

from config.settings import Settings
from config.tools_config import INTERRUPT_DESC



logger = logging.getLogger("agent")
console = Settings.console
checkpointer = PostgresSaver(Settings.postgres_connection)
checkpointer.setup()


class Agent:
    def __init__(self, model_provider:str, tools:list[dict], system_prompt: SystemMessage):

        self.model_provider = model_provider
        self.sys_prompt = system_prompt   
        self.tools = [tool["tool"] for tool in tools]
        self.checkpointer = checkpointer
        self.middlewares = [
            SummarizationMiddleware(model=self.model_provider, 
                                                     trigger = ("fraction", 0.5)), 
            HumanInTheLoopMiddleware(
                interrupt_on= {tool["tool"].name : tool["interrupt"] 
                               for tool in tools}
                               )
                            ]

        self.agent = create_agent(
                    self.model_provider,
                    system_prompt=self.sys_prompt,
                    tools=self.tools,
                    middleware=self.middlewares, 
                    checkpointer= self.checkpointer
                        )
        
        logger.info("agent initialized.")





    def run_step(self,  thread_id: str, messages: list):
        logger.debug("called Agent.run")
        config = {"configurable": {"thread_id": thread_id}}
        #initial run
        self._stream_agent({"messages": messages}, config)

        state = self.agent.get_state(config) #current state
        while state.next:  #there are nodes to execute
            if state.tasks:  # tool calls
                task = state.tasks[0]  #first pending task
                if task.interrupts:  # if interrupted
                    interrupt = task.interrupts[0]  # Interrupt object
                    action_requests = interrupt.value["action_requests"]  #tool calls needing approval
                    decisions = []
                    for request in action_requests:
                        human_decision = self._get_approval(request)
                        decisions.append(human_decision)
                    #resume 
                    self._stream_agent(input= Command(resume={"decisions":decisions}), config= config)
                
                else: 
                    self._stream_agent(None, config=config)
            
            else: 
                self._stream_agent(None, config=config)

            state = self.agent.get_state(config)  #refresh state



            



    def _stream_agent(self, input, config):
        #I use this bool to avoid printing "calling tools..." multiple times in a row
        called_tool = False
        with Live(console=console, refresh_per_second=15) as live:
            full_resp = ""
            for msg_chunk, metadata in self.agent.stream(input, stream_mode="messages", config=config):
                if isinstance(msg_chunk, AIMessageChunk):
                    if msg_chunk.content:
                        full_resp+= msg_chunk.content
                        live.update(Panel(
                                        Markdown(full_resp),
                                        title="SHEET",
                                        box=box.HEAVY,
                                        border_style="#00E5FF",
                                        padding=(0, 1),
                                        subtitle="[dim]type [bold white]/quit[/bold white] to quit",
                                        subtitle_align="center",
                                    ))
                        called_tool = False

                elif isinstance(msg_chunk, ToolMessage):
                    if not called_tool: 
                        #only print it if it's not the last thing printed
                        live.update(Markdown("*calling tools...*"), refresh=True)
                        called_tool = True





    def _get_approval(self, action): 
        """get human feedback regarding a risky tool"""
        desc = INTERRUPT_DESC.get(action['name'], "").upper()
        args_str = "\n"
        for arg in action['args']:
            args_str += f"- {arg}: `{action['args'][arg]}`   \n"
        panel = Panel(
                    Markdown(f"""*action*: **{desc}**  
                *args*:  {args_str}  \n"""),
                    title="APPROVAL NEEDED",
                    box=box.DOUBLE,
                    border_style="yellow",
                    padding=(0, 1),
                    subtitle="[dim]type [bold white]/reject[/bold white] to reject  ·  [dim]type [bold white]anything else[/bold white] to approve",
                    subtitle_align="center")
        
        console.print(panel)
        feedback = console.input("❯ ").strip().lower()
        if feedback == "/reject":
            console.print(Markdown("**REASON FOR REJECTION:**"))
            reason = console.input("❯ ")
            decision = {"type": "reject", "message": reason}

        # elif feedback == "e":
        #     new_args = console.input(Markdown("*enter new args as JSON (double quotes for arg names):* "))
        #     decision = {
        #         "type": "edit",
        #         "edited_action": {"name": action["name"], "args": json.loads(new_args)}
        #     }
            
        else: 
            decision = {"type": "approve"}
        
        return decision






    def generate_convo_title(self, user_1st_prompt : str): 
        model = init_chat_model(self.model_provider)
        response = model.invoke([SystemMessage(f"""generate a short title (5 words max) for a conversation
                                         that starts with: '{user_1st_prompt}'.
                                           reply with only the title, no quotes.""")])

        #remove reasoning 
        title = re.sub(r"<think>.*?</think>", "",
                        response.content, flags=re.DOTALL).strip()
        return title if title else "New Conversation"









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

