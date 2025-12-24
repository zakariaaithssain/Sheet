import gspread
from config.google_config import oauth_json, SCOPES


google_client = gspread.oauth(
            scopes=SCOPES,
            credentials_filename=oauth_json
            )