import json
import re


# Checks response for valid range, returns True if responses are 200 or 300
def check_response(response):
    pattern = re.compile(r'<Response\s*\[(?!([45][0-9][0-9]))\d{3}\]>')
    if pattern.match(str(response)) is not None:
        return True
    else:
        return False


def find_id_in_get(cur_id, name):
    result = False
    l_name = json.loads(name)
    for items in l_name:
        for values in items.values():
            if values == cur_id:
                result = True
                print(items)
    return result


def find_value_in_dict(to_find, json_object):
    result = None
    for key, value in json_object.items():
        if key == to_find:
            return value
        elif type(value) == dict:
            for in_key, in_value in value.items():
                if in_key == to_find:
                    return in_value
                elif type(in_value) == dict:
                    for iin_key,iin_value in in_value.items():
                        if iin_key == to_find:
                            return iin_value
    return result
