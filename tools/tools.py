import gspread
from gspread import Client


class ToolKit:
    def __init__(self, google_client: Client):
        self.google_client = google_client
        self.spreadsheet = None
        self.worksheet = None



    #whenever some method is called, self.spreadsheet and worksheet are set to the ones over which the method was called, so we keep track of last edited ones. 
    def get_active_sheets_metadata(self):
        return {
            "spreadsheet": (
                {
                    "title": self.spreadsheet.title,
                    "url": self.spreadsheet.url,
                    "last_update_time": self.spreadsheet.lastUpdateTime,
                }
                if self.spreadsheet
                else None
            ),
            "worksheet": (
                {
                    "title": self.worksheet.title,
                    "url": self.worksheet.url,
                }
                if self.worksheet
                else None
            ),
        }
    

    def set_active_sheet(self, spreadsheet:str, worksheet:str = None): 
        try:
            self.spreadsheet = self.google_client.open(spreadsheet)
            if worksheet: self.worksheet = self.spreadsheet.worksheet(worksheet)
            status = "done"
        except gspread.SpreadsheetNotFound:
            status= "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        finally:
            return {
            "status": status,
            "spreadsheet_url": self.spreadsheet.url
        }


        
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
                                                cols=len(headers), rows=31)
                #add header
                self.worksheet.update(values=[headers],
                                    range_name="A1:" + chr(64+len(headers)) + "1")
                self.worksheet.format("A1:" + chr(64+len(headers)) + "1", {'textFormat': {'bold': True}})
                
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
                status = "found"
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



    def insert_row(self, title: str, spreadsheet: str, data: dict): 
        try: 
            self.spreadsheet = self.google_client.open(title=spreadsheet)
            try:
                self.worksheet = self.spreadsheet.worksheet(title=title)
                #lower headers and data keys to compare
                sheet_headers = [header.lower() for header in self.worksheet.row_values(1)]
                lower_data = {k.lower(): v for k, v in data.items()}

                #data should be compatible with headers
                if all(header in sheet_headers for header in lower_data.keys()): 
                    #data should be in the order of the columns (some gspread limitations)
                    ordered_values = []
                    for header in sheet_headers: 
                        ordered_values.append(lower_data[header])

                    self.worksheet.append_row(ordered_values, table_range="A1")
                    status = "inserted"
        
                else: 
                    status = "mismatch between headers and data"

            except gspread.WorksheetNotFound: 
                status = "worksheet not found"

        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"

        except Exception as e: 
            status = e.args[0] 
        
        finally: 
            return {"worksheet": title, 
                    "spreadsheet": spreadsheet, 
                    "status": status, 
                    "headers": sheet_headers}
        
    

    def get_worksheet_data(self, title: str, spreadsheet: str): 
        try: 
            self.spreadsheet = self.google_client.open(title=spreadsheet)
            try:
                self.worksheet = self.spreadsheet.worksheet(title=title)
                data = self.worksheet.get_all_records(head=1)
                #add a row key to every dict representing a row
                for index, row in enumerate(data):
                    row["row"] = index +1

                status = "done"

            except gspread.WorksheetNotFound: 
                status = "worksheet not found"
                data = None

        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
            data = None

        except Exception as e: 
            status = e.args[0] 
            data = None

        finally: 
            return {"worksheet": title, 
                    "spreadsheet": spreadsheet, 
                    "status": status,
                    "data": data}

        
    



