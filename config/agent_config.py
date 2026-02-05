
from config.google_config import GOOGLE_CLIENT
from agent.tools import ToolKit

from langchain.tools import tool



toolkit = ToolKit(GOOGLE_CLIENT)
methods = [
    {"tool":toolkit.create_worksheet, 
     "desc": "create worksheet with given title and headers inside given spreadsheet"},

    {"tool":toolkit.create_spreadsheet,
      "desc": "create spreadsheet with given title"},

    {"tool":toolkit.delete_spreadsheet,
      "desc": "delete spreadsheet with given title"}, 

    {"tool":toolkit.delete_worksheet,
      "desc": "delete worksheet with given title if found in given spreadsheet"},

    {"tool":toolkit.list_spreadsheets,
      "desc": "list spreadsheets metadata",}, 

    {"tool":toolkit.list_worksheets,
      "desc": "list worksheets metadata belonging to given spreadsheet"},

    {"tool":toolkit.get_worksheet_headers,
      "desc": "get headers of given worksheet"},

    {"tool":toolkit.insert_row,
      "desc": "insert given data to new row in given worksheet"},

    {"tool":toolkit.get_worksheet_data,
      "desc": "get data from given worksheet"},

    {"tool":toolkit.get_active_sheets_metadata,
      "desc": "get metadata, including title, URL, last updated time, for context spreadsheet and worksheet"}, 

    {"tool":toolkit.set_active_sheet,
      "desc": "set context sheets to given sheets"},

    {"tool":toolkit.get_today_date,
      "desc": "get current day's date"},
    ]

TOOLS = []
#transform the methods to Langchain methods
#I can't decorate them directly in class definition, 
#because the decoration will consider the self as an arg
#so we need to instanciate the tools class first
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
    

#     }