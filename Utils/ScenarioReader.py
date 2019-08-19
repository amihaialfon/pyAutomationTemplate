import json
import os


def get_scenario_file():
    root = os.path.dirname(__file__)
    root = root.rstrip('\\Utils')
    filename = (root + '\\Sources\\scenario.json')
    with open(filename, 'r') as f:
        scenario = json.load(f)
        return scenario
