import os, yaml
from mover import Mover
from classifier import Classifier
from logger import Logger

class OrganizerBot:
    def __init__(self):
        print("Organizing your downloads folder...")

        try:
            with open("config.yaml", mode="r") as f:
                self.rules = yaml.safe_load(f) #safe_load() --> for config files
                self.downloads_path = self.rules["system_path"] + "Downloads"

            self.logger = Logger()
            self.bot_classifier = Classifier(self.rules, self.logger)
            self.mover = Mover(self.logger)
            
        except FileNotFoundError:
            print("'config.yaml' file does not exist in project directory. Please create yaml configuration file.")

    def organize_downloads(self):
        if not self.has_loose_files():
            return "Already organized, no loose files found!", self.logger.get_summary()
        
        for file_name in os.listdir(self.downloads_path):
            file_path = os.path.join(self.downloads_path, file_name)

            if not os.path.isdir(file_path):
                destination_path = self.bot_classifier.identify_destination(file_name)
                if destination_path == None:
                    continue
                self.mover.move_file(self.downloads_path, destination_path, file_name)

        self.logger.log_actions_into_sheets()
        return "Your files have been organized!", self.logger.get_summary()
    
    def has_loose_files(self):
        for item in os.scandir(self.downloads_path):
            if item.is_file():
                return True
        return False
