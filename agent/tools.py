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

        #spreadsheet title
        self.spread_title: str = "Monthly budget"
        #summary worksheet title
        self.summary_title: str = "Summary"
        #transactions worksheet title
        self.transactions_title: str = "Transactions"

        self.balance_cell: str = "L8"
        self.expenses_categ_range = "B28:B44"
        self.income_categ_range = "H28:H44"

        #variable li dayr 3liha lfilm 
        self.map = {}
        
        logger.info("ToolKit initialized.")

    
#======================== SUMMARY SHEET TOOLS ========================================


    #internal tool
    def _build_categs_map(self): 
        """
        should always be called before any change related to categories.   
        create a json schema of expense and income categories with corresponding indexes and save it to self.map
         """
        
        self.spreadsheet = self.google_client.open(self.spread_title)
        self.worksheet = self.spreadsheet.worksheet(self.summary_title)

        exp_categs = self.worksheet.get_values(range_name= self.expenses_categ_range)
        exp_map = {}
        for idx, categ in enumerate(exp_categs, start=28): 
            if categ[0]:
                exp_map[categ[0].lower().strip()] = idx
        self.map["expense"] = exp_map
        
        income_categs = self.worksheet.get_values(range_name= self.income_categ_range)
        income_map = {}
        for idx, categ in enumerate(income_categs, start=28): 
            if categ[0]:
                income_map[categ[0].lower().strip()] = idx
        self.map["income"] = income_map





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
            status = f"internal error: {e}" #this way the model would explain the error
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
            status = f"internal error: {e}" 
        return {
            "status": status, 
            "balance": balance if status == "done" else None
        }

        

        


    @log_tool(logger)
    def get_expenses_categories(self): 
        self._build_categs_map()
        categories = list(self.map['expense'].keys())
        
        return {
            "status": "done", 
            "expenses_categories": categories
        }

    


    @log_tool(logger)
    def get_income_categories(self): 
        self._build_categs_map()
        categories = list(self.map['income'].keys())
        
        return {
            "status": "done", 
            "income_categories": categories
        }




    @log_tool(logger)
    def get_planned_expenses(self): 
        try: 
            
            self.spreadsheet = self.google_client.open(title=self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)

            self._build_categs_map()
            categ_rows = self.map['expense']
            #the row index of the very last category to define the A1 notation range
            max_row_idx = max(categ_rows.values())
            range_name = f"B28:D{max_row_idx}"
            expenses_range = self.worksheet.get(range_name)
            expenses = {expense[0].lower().strip():expense[2] for expense in expenses_range}
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = f"internal error: {e}"
        
        return {
            "status": status, 
            "planned_expenses": expenses if status == "done" else None
        }



    @log_tool(logger)
    def get_actual_expenses(self): 
        try: 
            
            self.spreadsheet = self.google_client.open(title=self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)

            self._build_categs_map()
            categ_rows = self.map['expense']
            #the row index of the very last category to define the A1 notation range
            max_row_idx = max(categ_rows.values())
            range_name = f"B28:E{max_row_idx}"
            expenses_range = self.worksheet.get(range_name)
            expenses = {expense[0].lower().strip():expense[3] for expense in expenses_range}
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = f"internal error: {e}"
        
        return {
            "status": status, 
            "actual_expenses": expenses if status == "done" else None
        }




    @log_tool(logger)
    def get_planned_incomes(self): 
        try: 
            self.spreadsheet = self.google_client.open(title=self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)

            self._build_categs_map()
            categ_rows = self.map['income']
            #the row index of the very last category to define the A1 notation range
            max_row_idx = max(categ_rows.values())
            range_name = f"H28:J{max_row_idx}"
            income_range = self.worksheet.get(range_name)
            incomes = {income[0].lower().strip():income[2] for income in income_range}
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = f"internal error: {e}"
        
        return {
            "status": status, 
            "planned_incomes": incomes if status == "done" else None
        }
    



    @log_tool(logger)
    def get_actual_incomes(self): 
        try: 
            self.spreadsheet = self.google_client.open(title=self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)

            self._build_categs_map()
            categ_rows = self.map['income']
            #the row index of the very last category to define the A1 notation range
            max_row_idx = max(categ_rows.values())
            range_name = f"H28:K{max_row_idx}"
            income_range = self.worksheet.get(range_name)
            incomes = {income[0].lower().strip():income[3] for income in income_range}
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = f"internal error: {e}"
        
        return {
            "status": status, 
            "actual_incomes": incomes if status == "done" else None
        }



    
    @log_tool(logger)
    def set_planned_expense(self, expense_categ:str, planned_expense: float): 
        try: 
            self.spreadsheet = self.google_client.open(title=self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)

            self._build_categs_map()
            categ_row_idx = self.map["expense"][expense_categ.lower().strip()]
            expense_cell = f"D{categ_row_idx}"
            old_expense = self.worksheet.acell(expense_cell).value
            self.worksheet.update_acell(expense_cell, planned_expense)
            status = "done"
        except KeyError: 
            status = "category not found"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = f"internal error: {e}" 
                                    
        return {
                "expense_category": expense_categ,
                "new_planned_expense": planned_expense, 
                "old_planned_expense": old_expense, 
                "status": status
            } if status == "done" else {"status": status}





    @log_tool(logger)
    def set_planned_income(self, income_categ:str, planned_income: float): 
        try: 
            self.spreadsheet = self.google_client.open(title=self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(title=self.summary_title)

            self._build_categs_map()
            categ_row_idx = self.map["income"][income_categ.lower().strip()]
            income_cell = f"J{categ_row_idx}"
            old_income = self.worksheet.acell(income_cell).value
            self.worksheet.update_acell(income_cell, planned_income)
            status = "done"
        except KeyError: 
            status = "category not found"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = f"internal error: {e}" 
                                    
        return {
                "expense_category": income_categ,
                "new_planned_expense": planned_income, 
                "old_planned_expense": old_income, 
                "status": status
            } if status == "done" else {"status": status}








    @log_tool(logger)
    def create_expenses_categ(self, categ_name: str, planned_expense:float = 0): 
        try:
            self.spreadsheet = self.google_client.open(self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(self.summary_title)

            self._build_categs_map()
            last_categ_idx = max(self.map["expense"].values())

            name_cell = f"B{last_categ_idx + 1}"
            self.worksheet.update_acell(name_cell, categ_name)

            expense_cell = f"D{last_categ_idx + 1}"
            self.worksheet.update_acell(expense_cell, planned_expense)
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = f"internal error: {e}" 
            
        return {"status": status, 
                "categ_name": categ_name, 
                "planned_expense": planned_expense, 
                } 
    


    @log_tool(logger)
    def create_income_categ(self, categ_name: str, planned_income:float = 0): 
        try:
            self.spreadsheet = self.google_client.open(self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(self.summary_title)

            self._build_categs_map()
            last_categ_idx = max(self.map["income"].values())

            name_cell = f"H{last_categ_idx + 1}"
            self.worksheet.update_acell(name_cell, categ_name)

            income_cell = f"J{last_categ_idx + 1}"
            self.worksheet.update_acell(income_cell, planned_income)
            status = "done"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = f"internal error: {e}" 
            
        return {"status": status, 
                "categ_name": categ_name, 
                "planned_income": planned_income, 
                } 




    @log_tool(logger)
    def rename_expense_categ(self,old_name:str, new_name: str): 
        try:
            self.spreadsheet = self.google_client.open(self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(self.summary_title)

            self._build_categs_map()
            old_name = old_name.lower().strip()
            #this raises a key error if the old_name is not in the categories
            categ_index = self.map["expense"][old_name]
            name_cell = f"B{categ_index}"
            self.worksheet.update_acell(name_cell, new_name)
            status = "done"
        except KeyError: 
            status = "category not found"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = f"internal error: {e}" 
            
        return {"status": status, 
                "old_name": old_name, 
                "new_name": new_name, 
                } 
    

    

    @log_tool(logger)
    def rename_income_categ(self,old_name:str, new_name: str): 
        try:
            self.spreadsheet = self.google_client.open(self.spread_title)
            self.worksheet = self.spreadsheet.worksheet(self.summary_title)

            self._build_categs_map()
            old_name = old_name.lower().strip()
            #this raises a key error if the old_name is not in the categories
            categ_index = self.map["income"][old_name]
            name_cell = f"H{categ_index}"
            self.worksheet.update_acell(name_cell, new_name)
            status = "done"
        except KeyError: 
            status = "category not found"
        except gspread.SpreadsheetNotFound: 
            status = "spreadsheet not found"
        except gspread.WorksheetNotFound: 
            status = "worksheet not found"
        except Exception as e: 
            status = f"internal error: {e}" 
            
        return {"status": status, 
                "old_name": old_name, 
                "new_name": new_name, 
                } 

    

    @log_tool(logger)
    def delete_expense_categ(self,category:str): 
        """steps: if no transactions are associated:  
        - set planned expense to empty str   
        - rename to empty str  
        - sort to take resulted empty row to bottom. """
        status = "unknown internal error"
        category = category.lower().strip()
        #inside this, build_map is called, no need to call it again
        response = self.get_actual_expenses()
        #will be None if there was some prblm
        if isinstance(response["actual_expenses"], dict): 
            try:
                #raises keyerror if categ not found
                actual_expense = response["actual_expenses"][category]
                actual_expense_str = str(actual_expense).strip()
                # Handle empty strings, None, and other falsy values
                if actual_expense_str and actual_expense_str != "":
                    actual_expense = float(actual_expense_str.replace("$", "").replace(",", ""))
                else:
                    actual_expense = 0
                
                if actual_expense != 0: 
                    status = f"cannot delete category associated with transactions, associated expense: {actual_expense}"
                else: 
                    max_row = max(self.map["expense"].values()) 
                    #normally planned expense is a float, but setting it to an empty str erases the row
                    self.set_planned_expense(category, planned_expense="")
                    self.rename_expense_categ(category, new_name="")
                    
                    self.worksheet.sort((2, 'asc'), range=f"B28:F{max_row}")
                    status = "done"

            except KeyError: 
                status = "category not found"
            except Exception as e: 
                status = f"internal error: {e}" 
        else: 
            status = response["status"]
        
        return {"status" : status, 
                "category" : category}

                

    
    @log_tool(logger)
    def delete_income_categ(self,category:str): 
        """steps: if no transactions are associated:  
        - set planned income to empty str   
        - rename to empty str  
        - sort to take resulted empty row to bottom. """
        status = "unknown internal error"
        category = category.lower().strip()
        #inside this, build_map is called, no need to call it again
        response = self.get_actual_incomes()
        #will be None if there was some prblm
        if isinstance(response["actual_incomes"], dict): 
            try:
                #raises keyerror if categ not found
                actual_income = response["actual_incomes"][category]
                actual_income_str = str(actual_income).strip()
                # Handle empty strings, None, and other falsy values
                if actual_income_str and actual_income_str != "":
                    actual_income = float(actual_income_str.replace("$", "").replace(",", ""))
                else:
                    actual_income = 0
                
                if actual_income != 0: 
                    status = f"cannot delete category associated with transactions, associated income: {actual_income}"
                else: 
                    max_row = max(self.map["income"].values())
                    #normally planned income is a float, but setting it to an empty str erases the row
                    self.set_planned_income(category, planned_income="")
                    self.rename_income_categ(category, new_name="")
                    
                    self.worksheet.sort((8, 'asc'), range=f"H28:L{max_row}")
                    status = "done"

            except KeyError: 
                status = "category not found"
            except Exception as e: 
                status = f"internal error: {e}" 
        else: 
            status = response["status"]
        
        return {"status" : status, 
                "category" : category}

                    

   #======================== TRANSACTIONS SHEET TOOLS ========================================
    





#===============================GHAALIBAN MOHALSH NHTAJ HADSHY BAQI========================================================

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
            status = f"internal error: {e}" 
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
                    status = f"internal error: {e}"

        return {"spreadsheet": title, 
                "status": status}


    @log_tool(logger)
    def list_spreadsheets(self):
        try:
            spreadsheets = self.google_client.list_spreadsheet_files()
            spreadsheets_names = [ s["name"] for s in spreadsheets]
            status = "done"
        except Exception as e: 
            status = f"internal error: {e}"

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
            status = f"internal error: {e}"

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
            status = f"internal error: {e}" 
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
            status = f"internal error: {e}" 
        
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
            status = f"internal error: {e}" 
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
    

        
    



