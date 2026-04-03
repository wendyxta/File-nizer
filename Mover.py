import os

def move_file(downloads_dir, destination_dir, file_name):
    
    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)

    source_path = os.path.join(downloads_dir, file_name)
    destination_path = os.path.join(destination_dir, file_name)

    #skip non-files and duplicate files to prevent overwriting
    if not os.path.exists(source_path) or os.path.exists(destination_path):
        pass 

    os.rename(source_path, destination_path)

