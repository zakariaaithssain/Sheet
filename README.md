# Run `python main.py` to test the interactive CLI PoC  

if you encounter this error:  

 `google.auth.exceptions.RefreshError: ('invalid_grant: Token has been expired or revoked.')`   

then you need to run this to delete old oauth:  

`rm -rf ~/.config/gspread`  

after that run `python main.py` again.  



Right now, the model can only:
- Create spreadsheets
- Delete spreadsheets
- Create worksheets
- Delete worksheets
- List spreadsheets and their metadata
- List worksheets within a spreadsheet and their metadata

and understands all things associated with these actions
