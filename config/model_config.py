from sheets.tools import Tools
base_url = "https://api.groq.com/openai/v1"
model = "qwen/qwen3-32b"
#to prompt engineer the model for this specific project.
system_prompt = """Your name is GestAI, a financial assisstant. Your task is to help the user manage sheets in Google Spreadsheet.
- Always ask for missing information when needed. 
- Confirm the action before creating the sheet.
- Only provide instructions or call the "create_worksheet" function when you have all required parameters.
- Keep responses clear, concise, and user-friendly.
- Do not assume default values for title or columns; always ask the user.
- Only think when it's necessary, avoid unnecessary thinking.
- Make your responses direct, informative, and as short as possible.

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
      }
    },
    "required": ["title", "columns"]
  }
},

]

#map tool names to functions objects
google_client = Tools()
FUNCTIONS_MAP = {
    "create_worksheet" : google_client.create_worksheet
    }