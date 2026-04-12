from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import util

class Logger:
    def __init__(self):
        self.log = []
        self.source_path = "/Downloads"
        self.account_path = "service_account.json"
        self.spreadsheet_id = "1OjYhAYmgKgGBwV1IwA4TP_XTJXII6IAtQWt6kyPXNMw" 
        self.cell_range = "'Current Log'!A2"
        self.service = self.authenticate()
                         
    def get_summary(self):
        full_log = self.read_entries_from_sheets()
        total_files = len(full_log)

        today_files = 0
        today = str(datetime.now().strftime("%Y-%m-%d"))
        for entry in full_log:
            if entry[0].startswith(today):
                today_files+=1

        time_saved = total_files * 5 / 60 #assuming ~5 sec per file transfer
        return total_files, today_files, time_saved
    
    def read_entries_from_sheets(self):
        sheet = self.service.spreadsheets()
        entries = sheet.values().get(spreadsheetId=self.spreadsheet_id, range="'Current Log'!A2:G").execute()
        full_log = entries.get("values", [])
        return full_log

    def authenticate(self):
        scopes = ["https://www.googleapis.com/auth/spreadsheets"] #allow read and write access
        credentials = Credentials.from_service_account_file(self.account_path, scopes=scopes) 
        service = build("sheets", "v4", credentials=credentials) 
        return service
    
    def log_actions_into_sheets(self):
        rows = []
        header = ["Time", "File Name", "Action", "Result", "Source Path", "Destination Path", "Reason"]
        rows.append(header)
        for entry in self.log:
            rows.append(entry)

        sheet = self.service.spreadsheets()
        sheet.values().append(spreadsheetId=self.spreadsheet_id, 
                              range=self.cell_range, 
                              valueInputOption="RAW", 
                              body={"values": rows}).execute()

    def log_move(self, name, dest, reason="-", action="moved", result="success"):
        time = util.get_time()
        reformatted_src = util.format_src(self.source_path, name)
        reformatted_dest = util.format_dest(dest)

        entry = [time, name, action, result, reformatted_src, reformatted_dest, reason]
        self.log.append(entry)

    def log_skip(self, name, reason, dest="-", action="skipped", result="fail"):
        time = util.get_time()
        reformatted_src = util.format_src(self.source_path, name)
        reformatted_dest = util.format_dest(dest)

        entry = [time, name, action, result, reformatted_src, reformatted_dest, reason]
        self.log.append(entry)
