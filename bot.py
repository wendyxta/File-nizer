import os, yaml
import mover, logger
from classifier import Classifier

class OrganizerBot:
    def __init__(self):
        print("hi im OrganizerBot")

        with open("config.yaml", mode="r") as f:
            self.rules = yaml.safe_load(f) #safe_load() --> for config files
            self.downloads_path = self.rules["system_path"] + "Downloads"

        self.bot_classifier = Classifier(self.rules)

    def organize_downloads(self):
        for file_name in os.listdir(self.downloads_path):
            file_path = os.path.join(self.downloads_path, file_name)

            if not os.path.isdir(file_path):
                destination_path = self.bot_classifier.identify_destination(file_name)
                print(file_name + " --> " + destination_path)
                mover.move_file(self.downloads_path, destination_path, file_name)
                logger.log_action(self.downloads_path, destination_path)
    