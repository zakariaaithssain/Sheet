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
        try:
            #hna kan assumi bli spreadsheet whda kafya, m3a bzf d worksheets (per month?)
            self.spreadsheet = self.google_client.open("General Spreadsheet")
        except gspread.SpreadsheetNotFound:
            self.spreadsheet = self.google_client.create("General Spreadsheet")
        



    def create_worksheet(self, title: str, columns: list[str]) -> dict:
        try:
            self.worksheet: Worksheet = self.spreadsheet.add_worksheet(title=title,
                                             cols=len(columns), rows=1000)
            status = "created"
        except Exception as e: 
            #APIEroor is so broad, makaynash shy error specific l had lblan
            if "already exists" in str(e):
                self.worksheet = self.spreadsheet.worksheet(title=title)
                status = "exists"
            else: 
                raise
        #header
        self.worksheet.update(values=[columns],
                               range_name="A1:" + chr(64+len(columns)) + "1")
        
        return {
        "worksheet_title": self.worksheet.title,
        "status": status,
        "spreadsheet_url": self.spreadsheet.url
    }



if __name__ == "__main__": 
    print("creating a testing sheet")
    google = Tools()
    google.create_worksheet(title="test", columns=["test1", "test2", "test3"])