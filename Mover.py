import os

class Mover:
    def __init__(self, logger):
        self.logger = logger

    def move_file(self, downloads_dir, destination_dir, file_name):
        
        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir)

        source_path = os.path.join(downloads_dir, file_name)
        destination_path = os.path.join(destination_dir, file_name)

        #skip non-files and duplicate files to prevent overwriting
        if os.path.isdir(source_path):
            self.logger.log_skip(file_name, source_path, "file is a directory", destination_path)

        if not os.path.exists(source_path):
            self.logger.log_skip(file_name, source_path, "file no longer exists in the downloads directory", destination_path)

        if os.path.exists(destination_path):
            self.logger.log_skip(file_name, source_path, "file already exists at the destination directory", destination_path)

        os.rename(source_path, destination_path)
        self.logger.log_move(file_name, source_path, destination_path)
