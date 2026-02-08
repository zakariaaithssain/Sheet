# GestAI 

## how to run: 
- clone the repo
- then let uv do the rest: 
```bash 
uv sync
```
- run: 
```bash
uv run main.py
```


if you encounter this error:  

 `google.auth.exceptions.RefreshError: ('invalid_grant: Token has been expired or revoked.')`   

then you need to run this to delete old oauth config:  

`rm -rf ~/.config/gspread`  

after that run again, google authentication API popup will open, grant access to the app, and you're done. 



## Current Capabilities

The AI agent can perform the following operations:

**'MONTHLY BUDGET' SHEET SPECIFIC OPERATIONS:**
- Get and set starting balance
- Manage expense and income categories (get, create, rename, delete)
- Set planned expenses and incomes per category
- Track available slots for new categories

**Spreadsheet Management:**
- Create, delete, and list spreadsheets
- Retrieve spreadsheet metadata (name, ID, creation time, last modification)

**Worksheet Management:**
- Create, delete, and list worksheets within a spreadsheet
- Retrieve worksheet metadata (ID, title, index, column/row count)
- Access worksheet headers and data

**Data Operations:**
- Insert rows into worksheets
- Retrieve worksheet data
- Get current date context

**Context Awareness:**
- Track active spreadsheet and worksheet
- Retrieve active sheets metadata (title, URL, last modification time)

