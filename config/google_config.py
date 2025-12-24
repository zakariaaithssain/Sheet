from pathlib import Path

#the path to the Oauth json file.
oauth_json = Path("config/credentials/oauth.json")
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
           'https://www.googleapis.com/auth/drive']
