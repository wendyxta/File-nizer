from datetime import datetime
import os

def get_time():
    cur_datetime = datetime.today()
    return str(cur_datetime)

def format_src(source_path, name):
    src = source_path + "/" + name
    replaced_src = os.path.normpath(src).replace("/", "\\")
    return str(replaced_src)

def format_dest(dest):
    replaced_dest = "\\"+os.path.normpath(dest).replace("..\\", "")
    return str(replaced_dest)