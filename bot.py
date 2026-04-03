import os, yaml

class Bot:
    print("hi")

    with open("config.yaml", mode="r") as f:
        rules = yaml.safe_load(f) #safe_load() --> for config files

        downloads_path = rules["downloads_path"]

