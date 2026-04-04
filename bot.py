import os, yaml
from mover import Mover
from classifier import Classifier
from logger import Logger

class OrganizerBot:
    def __init__(self):
        print("Hi, I'm OrganizerBot!")

        try:
            with open("config.yaml", mode="r") as f:
                self.rules = yaml.safe_load(f) #safe_load() --> for config files
                self.downloads_path = self.rules["system_path"] + "Downloads"

            self.logger = Logger()
            self.bot_classifier = Classifier(self.rules, self.logger)
            self.mover = Mover(self.logger)
            
        except FileNotFoundError:
            print("'config.yaml' file does not exist in project directory. Please create configurations.")

    def organize_downloads(self):
        for file_name in os.listdir(self.downloads_path):
            file_path = os.path.join(self.downloads_path, file_name)

            if not os.path.isdir(file_path):
                destination_path = self.bot_classifier.identify_destination(file_name)
                self.mover.move_file(self.downloads_path, destination_path, file_name)
    