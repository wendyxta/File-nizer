import os, yaml
from mover import Mover
from classifier import Classifier
from logger import Logger

class OrganizerBot:
    """
    This class scans for loose files in a user's Downloads directory and automates the process of organizing the files.
    """

    def __init__(self):
        """
        Initializes an OrganizerBot instance with a shared Logger, Classifier, and Mover.
        Loads configuration ruels form the config.yaml file and handles missing config files.
        """
        try:
            with open("config.yaml", mode="r") as f:
                self.rules = yaml.safe_load(f) #safe_load() --> for config files
                self.downloads_path = self.rules["system_path"] + "Downloads"

            self.logger = Logger()
            self.classifier = Classifier(self.rules, self.logger)
            self.mover = Mover(self.logger)
            
        except FileNotFoundError:
            print("'config.yaml' file does not exist in project directory. Please create yaml configuration file.")

    def organize_downloads(self):
        """
        Organizes loose files inside the Downloads directory.
        - Iterates through all loose files in the Downloads directory
        - Extracts the name and extension of the file to classify the file destination
        - Moves the file to the destination directory if there is one 
        - Logs locally stored file actions into the cloud based spreadsheet
        - Generates a summary of file actions
        @return: a tuple containing a file system status message and the organization summary
        """
        if not self.has_loose_files():
            return "Already organized, no loose files found!", self.logger.get_summary()
        
        for file_name in os.listdir(self.downloads_path):
            file_path = os.path.join(self.downloads_path, file_name)

            if not os.path.isdir(file_path):
                destination_path = self.classifier.identify_destination(file_name)
                if destination_path == None:
                    continue
                self.mover.move_file(self.downloads_path, destination_path, file_name)

        self.logger.log_actions_into_sheets()
        return "Your files have been organized!", self.logger.get_summary()
    
    def has_loose_files(self):
        """
        Checks whether the Downloads directory contains loose files (not inside a subdirectory) to organize.
        @return: True if there are loose files, False otherwise
        """
        for item in os.scandir(self.downloads_path):
            if item.is_file() and self.classifier.valid_file_name(item.name):
                return True
        return False
