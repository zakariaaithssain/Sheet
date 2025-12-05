
base_url = "https://api.groq.com/openai/v1"
model = "qwen/qwen3-32b"

#to prompt engineer the model for this specific project.
system_prompt = """ """

#tools that will be defined in sheets/tools.py
#the best thing to do is to create these tools based on the gspread API docs: 
# https://docs.gspread.org/en/latest/

TOOLS = []

#map tool names to functions objects
FUNCTIONS = {}