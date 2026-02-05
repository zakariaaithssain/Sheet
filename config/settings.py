from os import getenv
import logging
import sys



from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    env: str = os.getenv("ENV", "dev")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # LLM
    model_name: str = os.getenv("MODEL_NAME", "gpt-4.1")
    temperature: float = float(os.getenv("TEMPERATURE", "0.2"))

    # Agent limits
    max_context_messages: int = int(os.getenv("MAX_CONTEXT_MESSAGES", "30"))



























#the only one needed by Langchain (API key is loaded directly)
MODEL_PROVIDER=getenv('MODEL_PROVIDER')



#no longer needed
model_api_key = getenv('MODEL_API_KEY')
model_base_url = getenv('MODEL_BASE_URL')
model_name = getenv('MODEL_NAME')


#logs
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_HANDLERS = [logging.StreamHandler(sys.stdout), #print
                logging.FileHandler("logs/app.log", mode="w") #write mode for dev 
                ]