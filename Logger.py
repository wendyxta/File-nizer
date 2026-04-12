from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import util

class Logger:
    """
    This class handles the logging of file operations and authentication and interaction with the Google Sheets API.
    """

    def __init__(self):
        """
        Initializes a Logger instance. Sets paths for the source path and service_account file. Authenticates the Google Sheets API client.
        """
        self.log = []
        self.source_path = "/Downloads"
        self.account_path = "service_account.json"
        self.spreadsheet_id = "1OjYhAYmgKgGBwV1IwA4TP_XTJXII6IAtQWt6kyPXNMw" 
        self.cell_range = "'Current Log'!A1"
        self.service = self.authenticate()
                         
    def get_summary(self):
        """
        Retrieves a summary of file system actions for today and all-time.
        @return: a tuple containing the total number of files organized, the number of files organzied today, and the amount of time saved (assuming ~10 sec per file transfer)
        """
        full_log = self.read_entries_from_sheets()
        total_files = 0
        today_files = 0

        today = str(datetime.now().strftime("%Y-%m-%d"))
        for entry in full_log[2:]:
            if len(entry)<2:
                continue

            if entry[2]=="moved":
                total_files+=1

                if entry[0].startswith(today): 
                    today_files+=1

        time_saved = total_files * 10 / 60 
        return total_files, today_files, time_saved
    
    def read_entries_from_sheets(self):
        """
        Retrieves all logged spreadsheet entries stored in Google Sheets.
        @return: a list containing each row of the spreadsheet
        """
        sheet = self.service.spreadsheets()
        entries = sheet.values().get(spreadsheetId=self.spreadsheet_id, range="'Current Log'!A2:G").execute()
        full_log = entries.get("values", [])
        return full_log

    def authenticate(self):
        """
        Authenticates with Google Sheets using service account credentials
        @return: the location of the googleapiclient.discovery.Resource object
        """
        scopes = ["https://www.googleapis.com/auth/spreadsheets"] #allow read and write access
        credentials = Credentials.from_service_account_file(self.account_path, scopes=scopes) 
        service = build("sheets", "v4", credentials=credentials) 
        return service
    
    def log_actions_into_sheets(self):
        """
        Uploads locally logged entries into Google Sheets document with a header row to indicate the start of each organization session.
        """
        rows = []
        header = ["Time", "File Name", "Action", "Reason", "Source Path", "Destination Path"]
        rows.append(header)
        for entry in self.log:
            rows.append(entry)

        sheet = self.service.spreadsheets()
        sheet.values().append(spreadsheetId=self.spreadsheet_id, 
                              range=self.cell_range, 
                              valueInputOption="RAW", 
                              body={"values": rows}).execute()

    def log_move(self, name, dest, reason="-", action="moved"):
        """
        Adds an entry to the local log storing timestamps, file names, and file paths of a file move.
        """
        time = util.get_time()
        reformatted_src = util.format_src(self.source_path, name)
        reformatted_dest = util.format_dest(dest)

        entry = [time, name, action, reason, reformatted_src, reformatted_dest]
        self.log.append(entry)

    def log_skip(self, name, reason, dest="-", action="skipped"):
        """
        Adds an entry to the local log storing timestamps, file names,  file paths, a reasons for a file skip.
        """
        time = util.get_time()
        reformatted_src = util.format_src(self.source_path, name)
        reformatted_dest = util.format_dest(dest)

        entry = [time, name, action, reason, reformatted_src, reformatted_dest]
        self.log.append(entry)
