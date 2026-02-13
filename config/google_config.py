import gspread
import os


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


#sheets and drive scope
SCOPES = gspread.auth.DEFAULT_SCOPES
GOOGLE_CLIENT = gspread.service_account_from_dict(info=CREDENTIALS, scopes=SCOPES)




