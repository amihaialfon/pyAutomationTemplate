import json
import os


def get_config():
    root = os.path.dirname(__file__)
    root = root.rstrip('\\Utils')
    filename = (root + '\\Sources\\Config.json')
    with open(filename, 'r') as f:
        config = json.load(f)
        return config
