import os, re

class Classifier:
    def __init__(self, config):
        self.config = config
        self.system_path = self.config["system_path"]

    def identify_destination(self, file_path):
        name_and_ext = os.path.basename(file_path).split(".")
        name = name_and_ext[0]
        ext = name_and_ext[1]

        new_path = self.check_extensions(ext)
        if new_path == None:
            new_path = self.check_keywords(name)
            if new_path == None:
                new_path = "Downloads/Misc" #default path if no rules match

        destination_path = self.system_path + new_path
        return destination_path

    # check if file extention is listed in config file
    def check_extensions(self, ext):
        config_ext = self.config["extensions"]

        if ext in config_ext.keys(): #use the assigned value as the destination
            return config_ext[ext]

    #check if file name contains a keyword listed in config file
    def check_keywords(self, name):
        adjusted_name = re.sub(r"[-._ ]", "", name).lower() #remove separators to match kw format
        print("adjusted ", adjusted_name)
        config_kw = self.config["keywords"]

        for kw in config_kw.keys():
            if kw in adjusted_name:
                return config_kw[kw]
