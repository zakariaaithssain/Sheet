import gspread
from config.google_config import oauth_json


google_client = gspread.oauth(
            scopes=['https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'],
            credentials_filename=oauth_json
            )