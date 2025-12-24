import gspread
from gspread import Client
#TODO: add more general purpose methods related to sheets management
#TODO: then move to specific ones: adding data etc.


class ToolKit:
    def __init__(self, google_client: Client):
        self.google_client = google_client


    
    def create_spreadsheet(self, title: str):
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
            "spreadsheet": self.spreadsheet.title
            }
        except gspread.SpreadsheetNotFound: 
            return {"status" : f"spreadsheet {spreadsheet} not found"}




    def delete_worksheet(self, title: str, spreadsheet: str):
        try: 
            self.spreadsheet = self.google_client.open(title=spreadsheet)
            try:
                self.worksheet = self.spreadsheet.worksheet(title=title)
                self.spreadsheet.del_worksheet(self.worksheet)
                status = "deleted"
            except gspread.WorksheetNotFound: 
                status = "not found"
            return {
            "worksheet_title": title,
            "status": status,
            "spreadsheet": spreadsheet
            }
        except gspread.SpreadsheetNotFound: 
            return {"worksheet_title": title,
                    "status": f"spreadsheet {spreadsheet} not found"}
        except Exception as e: 
            return {"worksheet_title": title,
                    "status": e.args[0]} #this way the model would explain the error
                            #because gspread don't separate technical errors
                            #from practical ones.



    def delete_spreadsheet(self, title: str): 
        try: 
            spread = self.google_client.open(title=title)
            self.google_client.del_spreadsheet(spread.id)
            status = "deleted"
        except gspread.SpreadsheetNotFound: 
            status = "not found"
        
        except Exception as e: 
                    status = e.args[0]

        return {"spreadsheet_title": title, 
                "status": status}
    

    

    def list_spreadsheets(self):
        spreadsheets = self.google_client.list_spreadsheet_files()

        spreadsheets_metadata = [
            {
                "id": s["id"],
                "name": s["name"],
                "created_time": s.get("createdTime"),
                "modified_time": s.get("modifiedTime"),
            }
               for s in spreadsheets]

        return {
            "spreadsheets_metadata": spreadsheets_metadata
        }

    
    def list_worksheets(self, spreadsheet: str):
        worksheets = self.google_client.open(title=spreadsheet).worksheets()

        worksheets_metadata = [
            {
                "id": ws.id,
                "title": ws.title,
                "index": ws.index,
                "rows": ws.row_count,
                "cols": ws.col_count,
                "sheet_type": ws._properties.get("sheetType"),
                "grid_properties": ws._properties.get("gridProperties"),
            }
            for ws in worksheets
        ]

        return {
            "spreadsheet": spreadsheet,
            "worksheets_metadata": worksheets_metadata,
        }





