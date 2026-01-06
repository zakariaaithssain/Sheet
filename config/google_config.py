from dotenv import load_dotenv
from tempfile import NamedTemporaryFile

import gspread
import json
import os

load_dotenv()
#why not just use the json file? because with docker that will be a pain in the ass. 
CREDENTIALS = {
    "installed":
        {
        "client_id":os.getenv("CLIENT_ID"),
        "project_id":os.getenv("PROJECT_ID"),
        "auth_uri":os.getenv("AUTH_URI"),
        "token_uri":os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url":os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_secret":os.getenv("CLIENT_SECRET"),
        "redirect_uris":[os.getenv("REDIRECT_URIS")]
        }
}

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
           'https://www.googleapis.com/auth/drive']

#oauth requires a json file, so we dump the credentials
try:
    with open('auth.json', 'w') as f: json.dump(CREDENTIALS, f)
    GOOGLE_CLIENT = gspread.oauth(scopes=SCOPES,
                                        credentials_filename= 'auth.json'
                                        )
    
finally: 
    if os.path.exists('auth.json'): os.remove('auth.json')




