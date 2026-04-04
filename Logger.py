from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

class Logger:
    def __init__(self):
        self.log = []
        self.account_path = "service_account.json"
        self.service = self.authenticate()

    def authenticate(self):
        scopes = ["https://www.googleapis.com/auth/spreadsheets"] #allow read and write access
        credentials = Credentials.from_service_account_file(self.account_path, scopes=scopes) 
        service = build("sheets", "v4", credentials=credentials) 
        return service
    
    def log_actions_into_sheets(self):
        spreadsheet_id = "1OjYhAYmgKgGBwV1IwA4TP_XTJXII6IAtQWt6kyPXNMw" 
        cell_range = "Sheet1!A2"

        rows = []
        header = ["Time", "File Name", "Action", "Result", "Reason", "Source Path", "Destination Path"]
        rows.append(header)

        for entry in self.log:
            rows.append(entry)

        sheet = self.service.spreadsheets()
        sheet.values().append(spreadsheetId=spreadsheet_id, 
                              range=cell_range, 
                              valueInputOption="RAW", 
                              body={"values": rows}).execute()

    def get_time(self):
        cur_datetime = datetime.today()
        return str(cur_datetime)

    def log_move(self, name, src, dest, reason="", action="moved", result="success"):
        time = self.get_time()
        entry = [time, name, action, result, src, dest, reason]
        self.log.append(entry)

    def log_skip(self, name, src, reason, dest="", action="skipped", result="fail"):
        time = self.get_time()
        entry = [time, name, action, result, src, dest, reason]
        self.log.append(entry)

    def log_misc(self, name, src, reason, dest, action="moved to misc", result="success"):
        time = self.get_time()
        entry = [time, name, action, result, src, dest, reason]
        self.log.append(entry)
