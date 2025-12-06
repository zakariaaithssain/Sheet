import gspread
from gspread import Worksheet
from google_auth_oauthlib.flow import InstalledAppFlow

from config.google_config import oauth_json

#functions li ghaycalli lmodel.

class Tools:

    def __init__(self):
        self.google_client = gspread.oauth(
            scopes=['https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'],
            credentials_filename=oauth_json)


    
    def create_spreadsheet(self, title):
        try:
            self.spreadsheet = self.google_client.open(title=title)
            status = "exists"
        except gspread.SpreadsheetNotFound:
            self.spreadsheet = self.google_client.create(title=title)
            status = "created"

        return {
        "spreadsheet_title": self.spreadsheet.title,
        "status": status,
        "spreadsheet_url": self.spreadsheet.url
    }
        
        



    def create_worksheet(self, title: str, columns: list[str], spreadsheet: str) -> dict:
        try: 
            self.spreadsheet = self.google_client.open(title=spreadsheet)
            try:
                self.spreadsheet.worksheet(title=title)
                status = "exists"
            except gspread.WorksheetNotFound: 
                self.worksheet = self.spreadsheet.add_worksheet(title=title,
                                                cols=len(columns), rows=1000)
                status = "created"
            #header
            self.worksheet.update(values=[columns],
                                range_name="A1:" + chr(64+len(columns)) + "1")
            
            return {
            "worksheet_title": self.worksheet.title,
            "status": status,
            "contained_in": self.spreadsheet.title
            }
        except gspread.SpreadsheetNotFound: 
            return {"status" : f"no spreadsheed titled {spreadsheet}, create it first"}


