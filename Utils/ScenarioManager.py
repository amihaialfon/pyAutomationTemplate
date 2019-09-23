import json
import os


def get_scenario_file(scenario_name):
    try:
        root = os.path.dirname(__file__)
        root = root.rstrip('\\Utils')
        filename = (root + '\\Sources\\' + scenario_name)
        with open(filename, 'r') as f:
            scenario = json.load(f)
            return scenario
    except IOError as e:
        print(e)


def get_file_path(in_filename):
    try:
        root = os.path.dirname(__file__)
        root = root.rstrip('\\Utils')
        filename = (root + '\\Sources\\' + in_filename)
        return filename
    except IOError as e:
        print(e)


def update_scenario_id(scenario, new_key, new_value):
    try:
        replace = {new_key: new_value}
        field_exists = False
        for key, value in scenario.items():
            if key == new_key:
                field_exists = True
        if field_exists:
            scenario.update(replace)
        return scenario
    except:
        print('Could not update scenario')


def scenario_compare(original_scenario, returned_scenario):
    try:
        identical = True
        for o_key, o_value in original_scenario.items():
            for r_key, r_value in returned_scenario.items():
                if o_key == r_key and o_key != 'createdAt' and r_key != 'updatedAt':
                    if o_value != r_value:
                        print('The different values are ' + str(o_value) + str(r_value))
                        identical = False
        return identical
    except:
        print('Could not compare scenarios due to some error')
