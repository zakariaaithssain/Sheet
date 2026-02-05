from dotenv import load_dotenv
from config.settings import Settings
from config.logging_config import setup_logging
from agent.runtime import AgentRuntime
from agent.memory import InMemoryConversationStore
from agent.agent import Agent
from interface import start_api





def main():
    load_dotenv()

    settings = Settings()
    setup_logging(settings)

    memory = InMemoryConversationStore(settings.max_context_messages)

    agent = Agent(
        model_provider=settings.model_provider, 
        tools=settings.tools, 
        system_prompt=settings.system_prompt
    )
    runtime = AgentRuntime(
        agent=agent, 
        memory=memory, 
        session_id="zakaria123"
    )

    start_api(runtime)

if __name__ == "__main__":
    main()








