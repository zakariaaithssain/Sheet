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

        self.expenses_categ_range = "B28:B41"
        self.planned_expenses_range = "B28:D41"

        self.income_categ_range = "H28:H33"
        self.planned_income_range = "H28:J33"

        self.categs_map = {
            "expenses": {
                "food": "D28",
                "gifts": "D29",
                "health/medical": "D30",
                "home": "D31",
                "transportation": "D32",
                "personal": "D33",
                "pets": "D34",
                "utilities": "D35",
                "travel": "D36",
                "debt": "D37",
                "other": "D38",
                #initial empty places to add new categs
                "empty": [
                {"cell": "B39", "planned_expense": "D39"},
                {"cell": "B40", "planned_expense": "D40"},
                {"cell": "B41", "planned_expense": "D41"}
                ],

                #when we add a new categ, it becomes renameable. add only the name
                "renameable": []
                },
                
            "income": {
                    "savings": "J28",
                    "paycheck": "J29",
                    "bonus": "J30",
                    "interest": "J31",
                    "other": "J32",

                    #only one place initial place to add new income categ
                    "empty": [
                        {"cell": "H33", "planned_income": "J33"}
                        ],

                    #add only the name
                    "renameable": []
                    },
        }


        self.renameable_expense_categs = self.categs_map["expenses"]["renameable"]
        self.empty_expense_categs_places = self.categs_map["expenses"]["empty"]

        self.renameable_income_categs = self.categs_map["income"]["renameable"]
        self.empty_income_categs_places = self.categs_map["income"]["empty"]
        
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
        


    @log_tool(logger)
    def get_expenses_categories(self): 
        try: 
            self.spreadsheet = self.google_client.open(title=self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)
            categories = self.worksheet.get(range_name=self.expenses_categ_range)
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = e.args[0]
        
        return {
            "status": status, 
            "expenses_categories": categories if status == "done" else None
        }

    


    @log_tool(logger)
    def get_income_categories(self): 
        try: 
            self.spreadsheet = self.google_client.open(title=self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)
            categories = self.worksheet.get(range_name=self.income_categ_range)
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = e.args[0]
        
        return {
            "status": status, 
            "income_categories": categories if status == "done" else None
        }


    @log_tool(logger)
    def get_planned_expenses(self): 
        try: 
            self.spreadsheet = self.google_client.open(title=self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)
            categories = self.worksheet.get(range_name=self.planned_expenses_range)
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = e.args[0]
        
        return {
            "status": status, 
            "planned_expenses": categories if status == "done" else None
        }


    @log_tool(logger)
    def get_planned_incomes(self): 
        try: 
            self.spreadsheet = self.google_client.open(title=self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)
            categories = self.worksheet.get(range_name=self.planned_income_range)
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = e.args[0]
        
        return {
            "status": status, 
            "planned_incomes": categories if status == "done" else None
        }
    

    
    @log_tool(logger)
    def set_planned_expense(self, expense_categ:str, planned_expense: float): 
        old_planned_expenses = self.get_planned_expenses()["planned_expenses"]
        if not old_planned_expenses:
            status = "category not found"
        else: 
            #we look for the categ, and get the old expense
            old_categ_expense = ''
            for categ in old_planned_expenses: 
                if categ[0].lower().strip() == expense_categ.lower().strip(): 
                    old_categ_expense = categ[-1]
                    break
            if old_categ_expense == '':
                status = "category not found"

            else:  
                try: 
                    expense_cell = self.categs_map["expenses"][expense_categ.lower().strip()]
                    self.spreadsheet = self.google_client.open(title=self.spread_title)
                    self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)
                    self.worksheet.update_acell(label=expense_cell, value=planned_expense)
                    status = "done"
                except gspread.SpreadsheetNotFound: 
                    status = "spreadsheet not found"
                except gspread.WorksheetNotFound: 
                    status = "worksheet not found"
                except Exception as e: 
                    status = e.args[0] 
                                   
        return {
                "expense_category": expense_categ,
                "new_planned_expense": planned_expense, 
                "old_planned_expense": old_categ_expense, 
                "status": status
            } if status == "done" else {"status": status}


    @log_tool(logger)
    def set_planned_income(self, income_categ:str, planned_income: float): 
        old_planned_incomes = self.get_planned_incomes()["planned_incomes"]
        if not old_planned_incomes:
            status = "category not found"
        else: 
            #we look for the categ, and get the old expense
            old_categ_income = ''
            for categ in old_planned_incomes: 
                if categ[0].lower().strip() == income_categ.lower().strip(): 
                    old_categ_income = categ[-1]
                    break
            if old_categ_income == '':
                status = "category not found"

            else:  
                try: 
                    income_cell = self.categs_map["income"][income_categ.lower().strip()]
                    self.spreadsheet = self.google_client.open(title=self.spread_title)
                    self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)
                    self.worksheet.update_acell(label=income_cell, value=planned_income)
                    status = "done"
                except gspread.SpreadsheetNotFound: 
                    status = "spreadsheet not found"
                except gspread.WorksheetNotFound: 
                    status = "worksheet not found"
                except Exception as e: 
                    status = e.args[0] 
                                   
        return {
                "income_category": income_categ,
                "new_planned_income": planned_income, 
                "old_planned_income": old_categ_income, 
                "status": status
            } if status == "done" else {"status": status}      


    @log_tool(logger)
    def get_renameable_categs(self):
        return {"renameable_expenses_categories": self.renameable_expense_categs, 
                "renameable_income_categories": self.renameable_income_categs}
    
    @log_tool(logger)
    def get_number_empty_categs_places(self):
        return {"empty_places_for_expenses_categories": len(self.empty_expense_categs_places), 
                "empty_places_for_income_categories": len(self.empty_income_categs_places)}



    @log_tool(logger)
    def add_new_expenses_categ(self, categ_name: str, planned_expense:float = 0): 
        empty_places = self.get_renameable_expenses_categs()["empty_places_to_add_new_categs"]
        if empty_places == 0: 
            status = "no empty places left"
        else: 
            try: 
                categ_name_cell = self.categs_map["expenses"][self.empty_expense_categs_places.pop()]["cell"]
                planned_expense_cell = self.categs_map["expenses"][self.empty_expense_categs_places]["planned_expense"]

                self.spreadsheet = self.google_client.open(title=self.spread_title)
                self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)
                #create categ name
                self.worksheet.update_acell(label=categ_name_cell, value=categ_name)
                #add planned expense: 
                self.worksheet.update_acell(label=planned_expense_cell, value=planned_expense)
                status = "done"
            except gspread.SpreadsheetNotFound: 
                status = "spreadsheet not found"
            except gspread.WorksheetNotFound: 
                status = "worksheet not found"
            except Exception as e: 
                status = e.args[0] 
            
            return {"status": status, 
                    "new_categ_name": categ_name, 
                    "new_categ_planned_expense": planned_expense, 
                    "empty_places_left": len(self.empty_expense_categs_places)} if status == "done" else {"status": status}




              

            

   
    


#=================================================

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
    

        
    



