# Sheet 

## setup:  

- create Google Cloud project  
- enable: Google Sheets API and Google Drive API.  
- Create Service Account  
- Download the JSON file and  use it to fill in the `.env` file (see `.env.example`)  
- create a `google drive folder` and put your sheets inside it  
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
#new conversation
uv run main.py 

#show past conversations and pick one to resume
uv run main.py --resume 
```
## run using Docker:   
*Note*: always use `docker compose run` (not `up`) to launch the app, it properly attaches the terminal for interactive input.

```bash
#new conversation
docker compose run --rm app

#show past conversations and pick one to resume
docker compose run --rm app --resume

#stop everything
docker compose down

#stop and wipe past conversations (all history is gone)
docker compose down -v 

```

## Current Capabilities

The AI agent can perform the following operations:

**Balance Management:**
- Get and set starting balance

**Categories Management:**
- Get expense and income categories
- Create expense and income categories
- Rename expense and income categories
- Delete expense and income categories (only if no transactions)

**Budget Planning:**
- Get planned and actual expenses and incomes
- Set planned expenses and incomes per category

**Transactions:**
- Add expense transactions
- Add income transactions

**Summary & Reporting:**
- Get comprehensive summary (remaining balance, savings, expenses, incomes)
- Get current date

**Spreadsheet Access:**
- List available spreadsheets
- List worksheets in a given spreadsheet
- Get spreadsheet and worksheet metadata (URL, title, last modification time)

