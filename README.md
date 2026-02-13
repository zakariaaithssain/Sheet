# GestAI 

## setup:  
- create a `google drive folder`
- share it with the `service account email` and give it editor access   

this setup will give the agent full access to `only the files inside that shared folder`.   

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


## Current Capabilities

The AI agent can perform the following operations:
- Get and set starting balance
- Get expense and income categories
- Get planned and actual expenses and incomes
- Set planned expenses and incomes per category
- Create, rename, and delete expense and income categories
- Add expense transactions
- List available spreadsheets
- List worksheets in a given spreadsheet
- Get spreadsheet and worksheet metadata
- Get current date

