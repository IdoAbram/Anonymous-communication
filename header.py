import random
import socket
import threading
import time
from datetime import datetime
import NetworkHandler as NH

class KeyReader:
    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r') as file:
            file_data = file.read()
        return file_data
def string_to_map(s):
    try:
        return eval(s)
    except Exception as e:
        print(f"Error converting string to map: {e}")
        return None

def convert_nested_strings(d):
    if isinstance(d, dict):
        for key, value in d.items():
            if isinstance(value, str):
                try:
                    d[key] = eval(value)
                except Exception:
                    pass  # Leave the value unchanged if it's not a valid dictionary string
            elif isinstance(value, dict):
                d[key] = convert_nested_strings(value)
    return d

def map_to_string(d):
    return str(d)