from datetime import datetime

class Logger:
    def __init__(self):
        self.log = []

    def get_log(self):
        return self.log

    def get_time(self):
        cur_datetime = datetime.today()
        return cur_datetime

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
