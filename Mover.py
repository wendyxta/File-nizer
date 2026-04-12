import os

class Mover:
    def __init__(self, logger):
        self.logger = logger

    def move_file(self, downloads_dir, destination_dir, file_name):
        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir)

        source_path = os.path.join(downloads_dir, file_name)
        destination_path = os.path.join(destination_dir, file_name)
        if not self.valid_path(source_path, destination_path, file_name):
            return

        os.rename(source_path, destination_path)
        self.logger.log_move(file_name, os.path.relpath(destination_path))

    #handle non-files and duplicate files to prevent overwriting
    def valid_path(self, source_path, destination_path, file_name):
        if os.path.isdir(source_path):
            self.logger.log_skip(file_name, "file is a directory", os.path.relpath(destination_path))
            return False
        
        if not os.path.exists(source_path):
            self.logger.log_skip(file_name, "file no longer exists in the downloads directory", os.path.relpath(destination_path))
            return False
        
        if os.path.exists(destination_path):
            self.logger.log_skip(file_name, "file already exists at the destination directory", os.path.relpath(destination_path))
            return False
        
        return True