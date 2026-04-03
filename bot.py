import os, yaml
import classifier, mover, logger

class OrganizerBot:
    def __init__(self):
        print("hi im OrganizerBot")

        with open("config.yaml", mode="r") as f:
            self.rules = yaml.safe_load(f) #safe_load() --> for config files
            self.downloads_path = self.rules["downloads_path"]

    def organize_downloads(self):
        for item in os.listdir(self.downloads_path):
            item_path = os.path.join(self.downloads_path, item)

            if not os.path.isdir(item_path):
                destination_path = classifier.identify_destination(item_path, self.rules)
                mover.move_file(self.downloads_path, destination_path)
                logger.log_action(self.downloads_path, destination_path)
    