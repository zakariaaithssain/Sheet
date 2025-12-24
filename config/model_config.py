from sheets.auth import google_client
from sheets.tools import ToolKit



base_url = "https://api.groq.com/openai/v1"
model = "qwen/qwen3-32b"


#to prompt engineer the model for this specific project.
system_prompt = """Your name is GestAI, a financial assistant. Your task is to help the user manage sheets in Google Sheets.
- Always ask for missing information when needed. 
- Confirm any action that might be risky.
- Only provide instructions or call the functions when you have all required parameters.
- Keep responses clear.
- Do not assume default values; always ask the user.
- Only think when it's necessary.
- Make your responses direct and as short as possible.
- Do not answer any questions that are out of your tasks.

"""




#tools that will be defined in sheets/tools.py
#gspread API docs: 
# https://docs.gspread.org/en/latest/

FUNCTIONS_DEF = [
    {
  "type": "function",
  "name": "create_worksheet",
  "description": "Create a worksheet with the given title and columns in the spreadsheet",
  "parameters": {
    "type": "object",
    "properties": {
      "title": {"type": "string", "description": "Worksheet title"},
      "columns": {
        "type": "array",
        "items": {"type": "string"},
        "description": "List of column headers"
      },
      "spreadsheet": {
          "type": "string", "description": "spreadsheet title in which to create the worksheet"}
    },
    "required": ["title", "columns", "spreadsheet"]
  }
},

{
  "type": "function",
  "name": "create_spreadsheet",
  "description": "Create a spreadsheet with the given title",
  "parameters": {
    "type": "object",
    "properties": {
      "title": {"type": "string", "description": "spreadsheet title"}
    },
    "required": ["title"]
  }
},

{
  "type": "function",
  "name": "delete_spreadsheet",
  "description": "delete a spreadsheet with the given title",
  "parameters": {
    "type": "object",
    "properties": {
      "title": {"type": "string", "description": "spreadsheet title"}
    },
    "required": ["title"]
  }
},

{
  "type": "function",
  "name": "delete_worksheet",
  "description": "delete a worksheet with the given title if found in the spreadsheet",
  "parameters": {
    "type": "object",
    "properties": {
      "title": {"type": "string", "description": "worksheet title"},
      "spreadsheet": {"type": "string", "description": "spreadsheet title in which to look for the worksheet"}
    },
    "required": ["title", "spreadsheet"]
  }
},
{
  "type": "function",
  "name": "list_spreadsheets",
  "description": "list all spreadsheets metadata owned by/shared with the user",
}, 
{
  "type": "function",
  "name": "list_worksheets",
  "description": "list all worksheets metadata in the given spreadsheet.",
  "parameters": {
    "type": "object",
    "properties": {
      "spreadsheet": {"type": "string", "description": "spreadsheet title in which to look for worksheets"}
    },
    "required": ["spreadsheet"]
  }
}
]

#map tool names to functions objects
toolkit = ToolKit(google_client)
FUNCTIONS_MAP = {
    "create_worksheet" : toolkit.create_worksheet,
    "create_spreadsheet":  toolkit.create_spreadsheet,
    "delete_spreadsheet": toolkit.delete_spreadsheet, 
    "delete_worksheet": toolkit.delete_worksheet,
    "list_spreadsheets": toolkit.list_spreadsheets, 
    "list_worksheets": toolkit.list_worksheets,
    }