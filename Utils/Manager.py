import json
import os


def get_file(name):
    try:
        root = os.path.dirname(__file__)
        root = root.rstrip('\\Utils')
        filename = (root + '\\Sources\\' + file_name)
        with open(filename, 'r') as f:
            name = json.load(f)
            return name
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



def id_compare(original_id, returned_id):
    try:
        identical = True
        for o_key, o_value in original_id.items():
            for r_key, r_value in returned_id.items():
                if o_key == r_key and o_key != 'createdAt' and r_key != 'updatedAt':
                    if o_value != r_value:
                        print('The different values are ' + str(o_value) + str(r_value))
                        identical = False
        return identical
    except:
        print('Could not compare ids due to some error')
