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



Right now, the model can only:
- Create spreadsheets
- Delete spreadsheets
- Create worksheets
- Delete worksheets
- List spreadsheets and their metadata
- List worksheets within a spreadsheet and their metadata
- Know worksheets headers
- Insert data into a worksheet

and understands all things associated with these actions
