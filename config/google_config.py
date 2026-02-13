import gspread
import json
import os
from dotenv import load_dotenv
from pathlib import Path

# #why not just use the json file? because with docker that will be a pain in the ^^. 
# CREDENTIALS = {
#     "installed":
#         {
#         "client_id":os.getenv("CLIENT_ID"),
#         "project_id":os.getenv("PROJECT_ID"),
#         "auth_uri":"https://accounts.google.com/o/oauth2/auth",
#         "token_uri":"https://oauth2.googleapis.com/token",
#         "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
#         "client_secret":os.getenv("CLIENT_SECRET"),
#         "redirect_uris":["http://localhost"]
#         }
# }

# Ensure project .env is loaded (useful when modules are imported before main())
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)

CREDENTIALS = {
  "project_id": os.getenv("PROJECT_ID"),
  "private_key_id": os.getenv("PRIVATE_KEY_ID"),
  "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
  "client_email": os.getenv("CLIENT_EMAIL"),
  "client_id": os.getenv("CLIENT_ID"),
  "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
  
  "type": "service_account",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
  "universe_domain": "googleapis.com"
}
missing = [k for k, v in CREDENTIALS.items() if not v]
if missing:
    raise ValueError(f"Missing env vars for keys: {missing}")



SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
GOOGLE_CLIENT = gspread.service_account_from_dict(info=CREDENTIALS, scopes=SCOPES)

# try:
#     with open('auth.json', 'w') as f: 
#         json.dump(CREDENTIALS, f)

    
# finally: 
#     if os.path.exists('auth.json'): os.remove('auth.json')




