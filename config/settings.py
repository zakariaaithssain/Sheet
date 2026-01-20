from os import getenv
import logging
import sys


#the only one needed by Langchain (API key is loaded directly)
MODEL_PROVIDER=getenv('MODEL_PROVIDER')



#no longer needed
model_api_key = getenv('MODEL_API_KEY')
model_base_url = getenv('MODEL_BASE_URL')
model_name = getenv('MODEL_NAME')


#logs
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_HANDLERS = [logging.StreamHandler(sys.stdout), #print
                logging.FileHandler("logs/app.log", mode="w") #write mode for dev 
                ]