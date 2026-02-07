from gspread import Client

import gspread
import datetime
import logging

from config.logging_config import log_tool


logger = logging.getLogger("tools")
""" NOTE: Whenever we add a method to this class, to make it a tool that is accessible for the 
agent, we need to configure it in the config/tools_config file."""

class ToolKit:
    def __init__(self, google_client: Client):
        self.google_client = google_client
        self.spreadsheet = None
        self.worksheet = None
        self.spread_title: str = "Monthly budget"
        self.summary_title: str = "Summary"
        self.transactions_title: str = "Transactions"
        self.balance_cell: str = "L8"
        logger.info("ToolKit initialized.")

    
    @log_tool(logger)
    def set_starting_balance(self, balance:float): 
        old_balance = self.get_starting_balance()["balance"]
        try: 
            self.spreadsheet = self.google_client.open(title=self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)
            self.worksheet.update_acell(label=self.balance_cell, value=balance)
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = e.args[0] #this way the model would explain the error
                            #because gspread don't separate technical errors
                            #from practical ones.
        return {
            "new_starting_balance": balance, 
            "old_starting_balance": old_balance, 
            "status": status
        }
        

    @log_tool(logger)
    def get_starting_balance(self): 
        try: 
            self.spreadsheet = self.google_client.open(title=self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)
            balance = self.worksheet.acell(label=self.balance_cell).value
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = e.args[0] 
        return {
            "status": status, 
            "balance": balance if status == "done" else None
        }
        

    


    #whenever some method is called, self.spreadsheet and worksheet are set to the ones over which the method was called, so we keep track of last edited ones. 
    @log_tool(logger)
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
    
    @log_tool(logger)
    def set_active_sheet(self, spreadsheet:str, worksheet:str = None): 
        try:
            self.spreadsheet = self.google_client.open(spreadsheet)
            if worksheet: self.worksheet = self.spreadsheet.worksheet(worksheet)
            status = "done"
        except gspread.SpreadsheetNotFound:
            status= "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"

        return {
        "status": status,
        "spreadsheet_url": self.spreadsheet.url if self.spreadsheet else None
    }


    @log_tool(logger)
    def create_spreadsheet(self, title: str):
        try:
            self.spreadsheet = self.google_client.open(title=title)
            status = "exists"
        except gspread.SpreadsheetNotFound:
            self.spreadsheet = self.google_client.create(title=title)
            status = "created"

        return {
        "spreadsheet": self.spreadsheet.title,
        "status": status,
        "spreadsheet_url": self.spreadsheet.url 
    }

        
        

    @log_tool(logger)
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
        
        return {
        "worksheet": title,
        "status": status,
        "spreadsheet": spreadsheet
        }


    @log_tool(logger)
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
            status = "spreadsheet not found"
        except Exception as e: 
            status = e.args[0] 
        return {
        "worksheet": title,
        "status": status,
        "spreadsheet": spreadsheet
        }


    @log_tool(logger)
    def delete_spreadsheet(self, title: str): 
        try: 
            spread = self.google_client.open(title=title)
            self.google_client.del_spreadsheet(spread.id)
            status = "deleted"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        
        except Exception as e: 
                    status = e.args[0]

        return {"spreadsheet": title, 
                "status": status}


    @log_tool(logger)
    def list_spreadsheets(self):
        try:
            spreadsheets = self.google_client.list_spreadsheet_files()
            spreadsheets_names = [ s["name"] for s in spreadsheets]
            status = "done"
        except Exception as e: 
            status = e.args[0]

        return {
            "status": status, 
            "available_spreadsheets" : spreadsheets_names if status == "done" else None
        }

    @log_tool(logger)
    def get_spreadsheet_metadata(self, spreadsheet:str): 
        try: 
            self.spreadsheet = self.google_client.open(spreadsheet)
            spreadsheet_metadata = {
                "id": self.spreadsheet.id,
                "name": spreadsheet,
                "creation_time": self.spreadsheet.creationTime,
                "last_modif_time": self.spreadsheet.lastUpdateTime,
            }
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"

        return {
            "status": status,
            "spreadsheet_metadata": spreadsheet_metadata if status == "done" else None
        }
    


    @log_tool(logger)
    def list_worksheets(self, spreadsheet: str):
        try:
            worksheets = self.google_client.open(title=spreadsheet).worksheets()
            worksheets_names = [ws.title for ws in worksheets]
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"

        except Exception as e: 
            status = e.args[0]

        return {
            "status": status, 
            "spreadsheet": spreadsheet,
            "available_worksheets" : worksheets_names if status == "done" else None
        }
    


    @log_tool(logger)
    def get_worksheet_metadata(self, title: str, spreadsheet:str): 
        try: 
            self.spreadsheet = self.google_client.open(spreadsheet)
            self.worksheet = self.spreadsheet.worksheet(title=title)
            worksheet_metadata = {
                "id": self.worksheet.id,
                "title": self.worksheet.title,
                "index": self.worksheet.index,
                "rows": self.worksheet.row_count,
                "cols": self.worksheet.col_count
            }
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        
        
        return {
            "status": status,
            "worksheet_metadata": worksheet_metadata if status == "done" else None
        }



    @log_tool(logger)
    def get_worksheet_headers(self, title:str, spreadsheet: str):
        try: 
            self.spreadsheet = self.google_client.open(title=spreadsheet)
            try:
                self.worksheet = self.spreadsheet.worksheet(title=title)
                headers = self.worksheet.row_values(1)
                if headers: status = "done"
                else: 
                    status = "headers not found"
            except gspread.WorksheetNotFound: 
                status = "worksheet not found"
                headers = None

        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
            headers = None
        except Exception as e: 
            status = e.args[0] 
            headers = None
        
        return {"worksheet": title, 
                "spreadsheet": spreadsheet, 
                "status": status, 
                "headers": headers}



    @log_tool(logger)
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
        
        return {"worksheet": title, 
                "spreadsheet": spreadsheet, 
                "status": status, 
                "headers": sheet_headers}
    
    

    @log_tool(logger)
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

        
        return {"worksheet": title, 
                "spreadsheet": spreadsheet, 
                "status": status,
                "data": data}
        


    @log_tool(logger)
    def get_today_date(self): 
        return {"status":"done", 
                "date": datetime.date.today().strftime("%d/%m/%Y")
                }


        
    



