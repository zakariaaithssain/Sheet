class AgentRuntime:
    def __init__(self, llm, memory, tools):
        self.llm = llm
        self.memory = memory
        self.tools = tools

    def step(self, session_id: str, user_input: str):
        messages = self.memory.load(session_id)
        messages.append({"role": "user", "content": user_input})

        response = self.llm.run(messages, tools=self.tools)

        messages.append({"role": "assistant", "content": response})
        self.memory.save(session_id, messages)

        return response
