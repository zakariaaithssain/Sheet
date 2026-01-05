import gspread
from gspread import Client


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
        finally:
            return {
            "spreadsheet": self.spreadsheet.title,
            "status": status,
            "spreadsheet_url": self.spreadsheet.url
        }
    
        
        



    def create_worksheet(self, title: str, headers: list[str], spreadsheet: str) -> dict:
        try: 
            self.spreadsheet = self.google_client.open(title=spreadsheet)
            try:
                self.worksheet = self.spreadsheet.worksheet(title=title)
                status = "exists"
            except gspread.WorksheetNotFound: 
                self.worksheet = self.spreadsheet.add_worksheet(title=title,
                                                cols=len(headers), rows=1000)
                #add header
                self.worksheet.update(values=[headers],
                                    range_name="A1:" + chr(64+len(headers)) + "1")
                
                status = "created"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        
        finally: 
            return {
            "worksheet": title,
            "status": status,
            "spreadsheet": spreadsheet
            }




    def delete_worksheet(self, title: str, spreadsheet: str):
        try: 
            self.spreadsheet = self.google_client.open(title=spreadsheet)
            try:
                self.worksheet = self.spreadsheet.worksheet(title=title)
                self.spreadsheet.del_worksheet(self.worksheet)
                status = "deleted"
            except gspread.WorksheetNotFound: 
                status = "worksheet not found"
        except gspread.SpreadsheetNotFound: 
            status = f"spreadsheet not found"
        except Exception as e: 
            status = e.args[0] #this way the model would explain the error
                            #because gspread don't separate technical errors
                            #from practical ones.
        finally: 
            return {
            "worksheet": title,
            "status": status,
            "spreadsheet": spreadsheet
            }



    def delete_spreadsheet(self, title: str): 
        try: 
            spread = self.google_client.open(title=title)
            self.google_client.del_spreadsheet(spread.id)
            status = "deleted"
        except gspread.SpreadsheetNotFound: 
            status = "not found"
        
        except Exception as e: 
                    status = e.args[0]

        finally: 
            return {"spreadsheet": title, 
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



    def get_worksheet_headers(self, title:str, spreadsheet: str):
        try: 
            self.spreadsheet = self.google_client.open(title=spreadsheet)
            try:
                self.worksheet = self.spreadsheet.worksheet(title=title)
                headers = self.worksheet.row_values(1)
                status = "done"
            except gspread.WorksheetNotFound: 
                status = "worksheet not found"
                headers = None

        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
            headers = None
        except Exception as e: 
            status = e.args[0] 
            headers = None
        
        finally: 
            return {"worksheet": title, 
                    "spreadsheet": spreadsheet, 
                    "status": status, 
                    "headers": headers}

    def insert_item(self, spreadsheet: str, worksheet: str, **kwargs): 
        ...




