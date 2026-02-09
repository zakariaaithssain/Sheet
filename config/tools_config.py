
from config.google_config import GOOGLE_CLIENT
from agent.tools import ToolKit

from langchain.tools import tool



"""
transform the ToolKit class methods to Langchain tools,
I can't decorate them directly in class definition, 
because the decoration will consider the self arg as a tool arg,
so we need to instanciate the class first

"""


toolkit = ToolKit(GOOGLE_CLIENT)
methods = [
    {"tool": toolkit.get_starting_balance, 
     "desc": "get the starting balance"},

     {"tool": toolkit.set_starting_balance, 
      "desc": "set the starting balance to given value"}, 

     {"tool": toolkit.get_expenses_categories, 
      "desc": "get expenses categories names"}, 

     {"tool": toolkit.get_income_categories, 
      "desc": "get income categories names"}, 

     {"tool": toolkit.get_planned_expenses, 
      "desc": "get planned expense per expense category"}, 

     {"tool": toolkit.get_planned_incomes, 
      "desc": "get planned income per income category"}, 

     {"tool": toolkit.set_planned_expense, 
      "desc": "set planned expense for given expense category"}, 

     {"tool": toolkit.set_planned_income, 
      "desc": "set planned income for given income category"}, 

    #  {"tool": toolkit.get_renameable_categs, 
    #   "desc": "get income and expenses categories that can be renamed. this is equivalent to categories created by the user, as the only categories that can be renamed are the ones created by the user, the rest are system defined and cannot be renamed"}, 

     {"tool": toolkit.count_empty_categs_places, 
      "desc": "get the number of places left to add new expenses and income categories"}, 

     {"tool": toolkit.create_expenses_categ, 
      "desc": "add new expenses category"}, 

     {"tool": toolkit.create_income_categ, 
      "desc": "add new income category"}, 

     {"tool": toolkit.rename_user_expense_categ, 
      "desc": "rename given expense category"}, 

     {"tool": toolkit.rename_user_income_categ, 
      "desc": "rename given income category"}, 

    #  {"tool": toolkit.delete_user_expense_categ, 
    #   "desc": "delete given expense category if possible"}, 

      {"tool": toolkit.delete_user_income_categ, 
      "desc": "delete given income category"}, 

     {"tool": toolkit.delete_expense_categ, 
      "desc": "delete given expense category"}, 






  #============================================

    {"tool":toolkit.create_worksheet, 
     "desc": "create worksheet with given title and headers inside given spreadsheet"},

    {"tool":toolkit.create_spreadsheet,
      "desc": "create spreadsheet with given title"},

    {"tool":toolkit.delete_spreadsheet,
      "desc": "delete spreadsheet with given title"}, 

    {"tool":toolkit.delete_worksheet,
      "desc": "delete worksheet with given title if found in given spreadsheet"},

    {"tool":toolkit.list_spreadsheets,
      "desc": "list available spreadsheets names"}, 

    {"tool": toolkit.get_spreadsheet_metadata, 
     "desc": "get given spreadsheet name, id, creation time, and last modification time"},

    {"tool":toolkit.list_worksheets,
      "desc": "list available worksheets names belonging to given spreadsheet"},

    {"tool":toolkit.list_worksheets,
      "desc": "list available worksheets names belonging to given spreadsheet"},
    
    {"tool": toolkit.get_worksheet_metadata, 
     "desc": "get given worksheet id, title, index inside given spreadsheet, no of cols and no of rows"},

    {"tool":toolkit.get_worksheet_headers,
      "desc": "get headers of given worksheet"},

    {"tool":toolkit.insert_row,
      "desc": "insert given data to new row in given worksheet"},

    {"tool":toolkit.get_worksheet_data,
      "desc": "get data from given worksheet"},

    {"tool":toolkit.get_active_sheets_metadata,
      "desc": "for context spreadsheet and worksheet, get title, URL, and last modification time if available"}, 

    #{"tool":toolkit.set_active_sheet,
     # "desc": "set context sheets to given sheets"},

    {"tool":toolkit.get_today_date,
      "desc": "get current day's date"},
    ]

TOOLS = []

for method in methods: 
    TOOLS.append(
                  tool(method["tool"], description=method["desc"])
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