
from config.google_config import GOOGLE_CLIENT

from agent.tools import ToolKit

from langchain.tools import tool
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme


"""
transform the ToolKit class methods to Langchain tools,
I can't decorate them directly in class definition, 
because the decoration will consider the self arg as a tool arg,
so we need to instanciate the class first

"""
#I cannot use the one defined in settings because of circular importing
console = Console(theme = Theme({
    "markdown.paragraph": "italic cyan",
    "markdown.h1": "bold magenta",
    "markdown.code": "yellow",
}))
console.print(Markdown("*fetching sheet state...*"))

toolkit = ToolKit(GOOGLE_CLIENT)
methods = [
  {"tool": toolkit.get_starting_balance, 
   "desc": "get the starting balance",
   "interrupt": False},

   {"tool": toolkit.set_starting_balance, 
    "desc": "set the starting balance to given value",
    "interrupt": True}, 

   {"tool": toolkit.get_expenses_categories, 
    "desc": "get expenses categories names",
    "interrupt": False}, 

   {"tool": toolkit.get_income_categories, 
    "desc": "get income categories names",
    "interrupt": False}, 

   {"tool": toolkit.get_planned_expenses, 
    "desc": "get planned expense per category",
    "interrupt": False}, 

   {"tool": toolkit.get_planned_incomes, 
    "desc": "get planned income per category",
    "interrupt": False}, 

   {"tool": toolkit.get_actual_expenses, 
    "desc": "get actual expenses per category calculated from transactions sheet",
    "interrupt": False}, 

   {"tool": toolkit.get_actual_incomes, 
    "desc": "get actual incomes per category calculated from transactions sheet",
    "interrupt": False}, 

   {"tool": toolkit.set_planned_expense, 
    "desc": "set planned expense for given expense category",
    "interrupt": True}, 

   {"tool": toolkit.set_planned_income, 
    "desc": "set planned income for given income category",
    "interrupt": True}, 

   {"tool": toolkit.create_expense_categs, 
    "desc": "add given expenses categories",
    "interrupt": True}, 

   {"tool": toolkit.create_income_categs, 
    "desc": "add given income categories",
    "interrupt": True}, 

   {"tool": toolkit.rename_expense_categ, 
    "desc": "rename given expense category",
    "interrupt": True}, 

   {"tool": toolkit.rename_income_categ, 
    "desc": "rename given income category",
    "interrupt": True}, 
    
    {"tool": toolkit.delete_income_categs, 
    "desc": "delete given income categories",
    "interrupt": True}, 

   {"tool": toolkit.delete_expense_categs, 
    "desc": "delete given expense categories",
    "interrupt": True},

    {"tool": toolkit.get_summary, 
     "desc": "get a summary of current state: remaining balance, current saving, decrease in total saving, and total planned (resp. actual) expenses and income",
     "interrupt": False},

    {"tool": toolkit.add_expense_transactions, 
    "desc": "add given expenses to transactions sheet",
    "interrupt": True},

    {"tool": toolkit.add_income_transactions, 
    "desc": "add given incomes to transactions sheet",
    "interrupt": True},

  {"tool":toolkit.get_today_date,
    "desc": "get current day's date",
    "interrupt": False},

   {"tool":toolkit.list_spreadsheets,
    "desc": "list available spreadsheets names",
    "interrupt": False}, 

  {"tool":toolkit.list_worksheets,
    "desc": "list available worksheets names belonging to given spreadsheet",
    "interrupt": False},
  
  {"tool":toolkit.get_sheets_metadata,
    "desc": "get URL, title and last modification time if available for given sheets",
    "interrupt": False},
]

TOOLS = []

for method in methods: 
    TOOLS.append(
                  {
                    "tool": tool(method["tool"], description=method["desc"]), 
                   "interrupt": method["interrupt"]
                   }
        )














#DEPRECATED (I USED IT BEFORE SWITCHING TO LANGCHAIN THAT WILL HANDLE ALL THIS FOR ME)

#tools that will be defined in sheets/tools.py
#gspread API docs: 
# https://docs.gspread.org/en/latest/

# FUNCTIONS_DEF = [
#     {
#   "type": "function",
#   "name": "create_worksheet",
#   "description": "Create a worksheet with the given title and headers in the spreadsheet",
#   "parameters": {
#     "type": "object",
#     "properties": {
#       "title": {"type": "string", "description": "Worksheet title"},
#       "headers": {
#         "type": "array",
#         "items": {"type": "string"},
#         "description": "List of column headers"
#       },
#       "spreadsheet": {
#           "type": "string", "description": "spreadsheet title in which to create the worksheet"}
#     },
#     "required": ["title", "headers", "spreadsheet"]
#   }
# },

# {
#   "type": "function",
#   "name": "create_spreadsheet",
#   "description": "Create a spreadsheet with the given title",
#   "parameters": {
#     "type": "object",
#     "properties": {
#       "title": {"type": "string", "description": "spreadsheet title"}
#     },
#     "required": ["title"]
#   }
# },

# {
#   "type": "function",
#   "name": "delete_spreadsheet",
#   "description": "delete a spreadsheet with the given title",
#   "parameters": {
#     "type": "object",
#     "properties": {
#       "title": {"type": "string", "description": "spreadsheet title"}
#     },
#     "required": ["title"]
#   }
# },

# {
#   "type": "function",
#   "name": "delete_worksheet",
#   "description": "delete a worksheet with the given title if found in the spreadsheet",
#   "parameters": {
#     "type": "object",
#     "properties": {
#       "title": {"type": "string", "description": "worksheet title"},
#       "spreadsheet": {"type": "string", "description": "spreadsheet title in which to look for the worksheet"}
#     },
#     "required": ["title", "spreadsheet"]
#   }
# },
# {
#   "type": "function",
#   "name": "list_spreadsheets",
#   "description": "list all spreadsheets metadata owned by/shared with the user",
# }, 
# {
#   "type": "function",
#   "name": "list_worksheets",
#   "description": "list all worksheets metadata in the given spreadsheet.",
#   "parameters": {
#     "type": "object",
#     "properties": {
#       "spreadsheet": {"type": "string", "description": "spreadsheet title in which to look for worksheets"}
#     },
#     "required": ["spreadsheet"]
#   }
# }, 
# {
#   "type": "function",
#   "name": "get_worksheet_headers",
#   "description": "get headers of a given worksheet",
#   "parameters": {
#     "type": "object",
#     "properties": {
#       "title": {"type": "string", "description": "worksheet title"}, 
#       "spreadsheet": {"type": "string", "description": "spreadsheet title in which to look for worksheet"}
#     },
#     "required": ["title", "spreadsheet"]
#   }
# }, 
# {
#   "type": "function",
#   "name": "insert_row",
#   "description": "insert data to new row in given worksheet",
#   "parameters": {
#     "type": "object",
#     "properties": {
#       "title": {"type": "string", "description": "worksheet title"}, 
#       "spreadsheet": {"type": "string", "description": "spreadsheet title in which to look for worksheet"}, 
#       "data": {"type":"object", "description": "dictionary of key-value pairs"}
#     },
#     "required": ["title", "spreadsheet", "data"]
#   },
# },
# {
#   "type": "function",
#   "name": "get_worksheet_data",
#   "description": "get all rows data from a given worksheet",
#   "parameters": {
#     "type": "object",
#     "properties": {
#       "title": {"type": "string", "description": "worksheet title"}, 
#       "spreadsheet": {"type": "string", "description": "spreadsheet title in which to look for worksheet"}, 
#     },
#     "required": ["title", "spreadsheet"]
#   },
# }, 

# {
#   "type": "function",
#   "name": "get_active_sheets_metadata",
#   "description": "get metadata for the currently active spreadsheet and worksheet, including titles, URLs, and last updated.",
# },
# {
#   "type": "function",
#   "name": "set_active_sheet",
#   "description": "set context active spreadsheet or/and worksheet",
#   "parameters": {
#     "type": "object",
#     "properties": {
#       "spreadsheet": {"type": "string", "description": "spreadsheet title to consider"}, 
#       "worksheet": {"type": "string", "description": "worksheet title"}, 
#     },
#     "required": ["spreadsheet"]
#   },
# }, 
# {
#   "type": "function",
#   "name": "get_today_date",
#   "description": "get today's date",
# }, 

# ]

# #map tool names to functions objects
# toolkit = ToolKit(GOOGLE_CLIENT)
# FUNCTIONS_MAP = {
#     "create_worksheet" : toolkit.create_worksheet,
#     "create_spreadsheet":  toolkit.create_spreadsheet,
#     "delete_spreadsheet": toolkit.delete_spreadsheet, 
#     "delete_worksheet": toolkit.delete_worksheet,
#     "list_spreadsheets": toolkit.list_spreadsheets, 
#     "list_worksheets": toolkit.list_worksheets,
#     "get_worksheet_headers": toolkit.get_worksheet_headers,
#     "insert_row": toolkit.insert_row,
#     "get_worksheet_data": toolkit.get_worksheet_data,
#     "get_active_sheets_metadata": toolkit.get_active_sheets_metadata, 
#     "set_active_sheet": toolkit.set_active_sheet,
#     "get_today_date": toolkit.get_today_date,
#     "get_active_sheets_metadata": toolkit.get_active_sheets_metadata, 
#     "set_active_sheet": toolkit.set_active_sheet,
#     "get_today_date": toolkit.get_today_date,
    

#     }