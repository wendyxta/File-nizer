class Logger:
    def __init__(self):
        self.log = []

    def log_time(self):
        pass

    def log_move(self, name, src, dest, action="move", result="success", reason=""):
        pass

    def log_skip(self, name, src, reason, dest="", action="skip", result="fail"):
        pass

    def log_error(self, name, src, reason, dest="", action="error", result="fail"):
        pass

    #logging format: time filename action success/fail srcpath destpath reason(skip/error)
