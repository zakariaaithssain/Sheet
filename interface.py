from agent.runtime import AgentRuntime


def start_api(agent_runtime:AgentRuntime):
        while True: 
            with agent_runtime as runtime: 
                user_input = str(input("(q to quit)\n"))
                if user_input.strip() in "qQ":
                    exit(0)
                else:
                    runtime.step(user_input)
                    print("\n")
