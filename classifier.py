import re

class Classifier:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.system_path = self.config["system_path"]
        self.default_path = "Downloads/Misc"

    def identify_destination(self, file_name): 
        if not self.valid_file_name(file_name):
            return None
        
        name_and_ext = file_name.rsplit(".", 1) #handle file names with mulitple dots: split from right to left, only 1x
        name = name_and_ext[0]
        ext = name_and_ext[1]

        new_path = self.check_extensions(ext)
        if new_path == None:
            new_path = self.check_keywords(name)
            if new_path == None:
                new_path = self.default_path #default path if no rules match

        destination_path = self.system_path + new_path
        return destination_path

    # handle file names missing name, missing extension --> use default path
    def valid_file_name(self, file_name):
        if not "." in file_name or file_name.endswith("."):
            self.logger.log_skip(file_name, "file is missing an extension")
            return False
        if file_name.startswith(".") or file_name == " ": 
            self.logger.log_skip(file_name, "file is missing a name")
            return False
        return True

    # check if file extention is listed in config file
    def check_extensions(self, ext):
        config_ext = self.config["extensions"]

        if ext in config_ext.keys(): #use the assigned value as the destination
            return config_ext[ext]

    #check if file name contains a keyword listed in config file
    def check_keywords(self, name):
        adjusted_name = re.sub(r"[-._ ]", "", name).lower() #remove separators to match kw format
        config_kw = self.config["keywords"]

        for kw in config_kw.keys():
            if kw in adjusted_name:
                return config_kw[kw]
