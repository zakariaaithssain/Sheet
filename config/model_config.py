from sheets.tools import Tools
base_url = "https://api.groq.com/openai/v1"
model = "qwen/qwen3-32b"
#to prompt engineer the model for this specific project.
system_prompt = """You are a Python assistant. Only use the provided functions to interact with Google Sheets. 
- Use create_worksheet(title, columns) to create sheets or get existing ones. 
- Always return results as JSON. 
- Do not assume anything outside the spreadsheet. 
- No explanations, just function calls and data, minimize responses.
- No unnecessary thinking, think only when you REALLY need to.
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