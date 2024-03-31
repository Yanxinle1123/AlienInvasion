import os
import sys


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


def user_home_path(dst_file_name):
    home_dir = os.path.expanduser("~")
    last_path = os.path.join(home_dir, dst_file_name)
    return last_path
