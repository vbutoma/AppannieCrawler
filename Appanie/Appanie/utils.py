import json
from functools import wraps
import os
import time


def log_time(func):
    # TODO: remove all logs to logger singleton class
    @wraps(func)
    def logged(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        finish_time = time.time()
        print('{}: Execution time of method {} is {} s'.format(
            args[0].__class__.__name__,
            func.__name__,
            round(finish_time - start_time, 5)
        ))
        return result

    return logged


# Function to safely extract a value from a dictionary by key, if it exists
def safe_extract(dictionary, key_a, key_b, v_id, default_type="str"):
    if key_a in dictionary and key_b in dictionary[key_a]:
        return dictionary[key_a][key_b]
    return "" if default_type == "str" else "0"


def load_json(file_path):
    """
    Loads JSON from the file
    :param file_path: path to JSON
    :return: JSON obj
    """
    return json.load(open(file_path, 'r')) if os.path.exists(file_path) else {}


def generate_relative_path(source_file, destination_file):
    """ Generate the full path name of a destination file in the same directory as the source file """
    return os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(source_file))), destination_file)
