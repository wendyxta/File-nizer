import os

class Mover:
    """
    This class checks file paths and moves files from their source path to their destination path.
    """

    def __init__(self, logger):
        """
        Initializes a Mover instance containing a shared logger.
        """
        self.logger = logger

    def move_file(self, downloads_dir, destination_dir, file_name):
        """
        Moves files from their source path to thier destination path and logs the destination path.
        Creates a new subdirectory at the destination directory if no path exists.
        Skips over invalid paths.
        """
        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir)

        source_path = os.path.join(downloads_dir, file_name)
        destination_path = os.path.join(destination_dir, file_name)
        if not self.valid_path(source_path, destination_path, file_name):
            return

        os.rename(source_path, destination_path)
        self.logger.log_move(file_name, os.path.relpath(destination_path))

    def valid_path(self, source_path, destination_path, file_name):
        """
        Handes non-files (directories) and duplicate files to prevent overwriting by logging a skip.
        @return: True is the file path is valid and exists, and False otherwise
        """
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