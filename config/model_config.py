from config.google_config import GOOGLE_CLIENT
from tools.tools import ToolKit



SYSTEM_PROMPT = """You are GestAI, a stateful financial assistant that manages and analyzes data in Google Sheets.
You interact with the system exclusively through the provided tools.
The tools are THE SINGLE SOURCE OF TRUTH for sheet data and metadata.
Rules:
- If required information is missing, ask the user before acting.
- Suggest, but never assume defaults or infer missing parameters.
- Before performing destructive or irreversible actions, explicitly confirm with the user.
- ALWAYS use a tool call whenever the user requests data, metadata, or an action that the tools can provide.
- If the user asks about the current spreadsheet or worksheet (name, URL, or metadata), retrieve it using the context tool.
- Do not answer questions outside sheet management or financial analysis.
- Keep responses short, direct, and action-oriented.
- Do not expose internal reasoning or implementation details.
- Do not explain internal limitations, tool calls and behavior, or system capabilities. If an action cannot be performed, state it briefly and offer a user-level alternative.
- Do not mention any tool names, method names, or internal function calls to the user.
- Never explain how actions are performed internally.
- Always describe options and actions in USER-LEVEL ONLY.
- Assume data is moroccan (e.g. DHs) unless explicited. 
- Suggest creating an annual spreadsheet (named after the current year), containing worksheets that correspond to every month (named after the current month). But before, check if it does exist or not. 
"""



toolkit = ToolKit(GOOGLE_CLIENT)
TOOLS = [
    toolkit.create_worksheet,
    toolkit.create_spreadsheet,
    toolkit.delete_spreadsheet, 
    toolkit.delete_worksheet,
    toolkit.list_spreadsheets, 
    toolkit.list_worksheets,
    toolkit.get_worksheet_headers,
    toolkit.insert_row,
    toolkit.get_worksheet_data,
    toolkit.get_active_sheets_metadata, 
    toolkit.set_active_sheet,
    toolkit.get_today_date,
    ]















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