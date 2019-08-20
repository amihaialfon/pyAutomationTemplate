import json
import os


def get_scenario_file():
    root = os.path.dirname(__file__)
    root = root.rstrip('\\Utils')
    filename = (root + '\\Sources\\scenario.json')
    with open(filename, 'r') as f:
        scenario = json.load(f)
        return scenario


def update_scenario_id(scenario, new_key, new_value):
    replace = {new_key: new_value}
    field_exists = False
    for key, value in scenario.items():
        if key == new_key:
            field_exists = True
    if field_exists:
        scenario.update(replace)
    return scenario


def scenario_compare(original_scenario, returned_scenario):
    identical = True
    for o_key, o_value in original_scenario.items():
        for r_key, r_value in returned_scenario.items():
            if o_key == r_key and o_key != 'createdAt' and r_key != 'updatedAt':
                if o_value != r_value:
                    print('The different values are ' + str(o_value) + str(r_value))
                    identical = False
    return identical
