from datetime import datetime
import os

"""
This file contains utility methods for formatting file paths and getting the current time.
"""

def get_time():
    """
    Retrieves the current date and time of file action and formats as YYYY-MM-DD HH:MM AM/PM
    @return: the current date and time
    """
    cur_datetime = datetime.today().strftime("%Y-%m-%d %I:%M %p")
    return str(cur_datetime)

def format_src(source_path, name):
    """
    Formats the source file path to replace forwardslashes with backslashes.
    @return: the formatted source path
    """
    src = source_path + "/" + name
    replaced_src = os.path.normpath(src).replace("/", "\\")
    return str(replaced_src)

def format_dest(dest):
    """
    Formats the destination file path to remove extra symbols.
    @return: the formatted destination path
    """
    replaced_dest = "\\"+os.path.normpath(dest).replace("..\\", "")
    return str(replaced_dest)