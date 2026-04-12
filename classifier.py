import re

class Classifier:
    """
    This class checks file name and extension and classifies where files should be moved to. 
    """

    def __init__(self, config, logger):
        """
        Initializes a Classifier instance containing a shared configuation and logger instance, and sets the default system path and default destination path.
        """
        self.config = config
        self.logger = logger
        self.system_path = self.config["system_path"]
        self.default_path = self.config["default_path"]

    def identify_destination(self, file_name): 
        """
        Determines the destination path for the file.
        @return: the corresponding path from the config file or the default path if not matches occur.
        """
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

    def valid_file_name(self, file_name):
        """
        Checks for a valid file name (includes both a name + file extension), and logs a skip otherwise.
        @return: True if the file name is valid, False otherwise
        """
        if not "." in file_name or file_name.endswith("."):
            self.logger.log_skip(file_name, "file is missing an extension")
            return False
        if file_name.startswith(".") or file_name == " ": 
            self.logger.log_skip(file_name, "file is missing a name")
            return False
        return True

    def check_extensions(self, ext):
        """Checks if file extention is listed in the config.yaml file.
        @return: corresponding value in teh config file as the destination path
        """
        config_ext = self.config["extensions"]

        if ext in config_ext.keys():
            return config_ext[ext]

    def check_keywords(self, name):
        """Checks if file name contains a keyword listed in the config.yaml file. 
        Reformats the file name if it contains separators or uppercase letters to match keyword format in the config file.
        @return: corresponding value in teh config file as the destination path
        """
        adjusted_name = re.sub(r"[-._ ]", "", name).lower() 
        config_kw = self.config["keywords"]

        for kw in config_kw.keys():
            if kw in adjusted_name:
                return config_kw[kw]
