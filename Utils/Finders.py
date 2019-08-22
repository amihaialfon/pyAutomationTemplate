import json
import re


# Checks response for valid range, returns True if responses are 200 or 300
def check_response(response):
    pattern = re.compile(r'<Response\s*\[(?!([45][0-9][0-9]))\d{3}\]>')
    if pattern.match(response) is not None:
        return True
    else:
        return False


def find_id_in_scenario_get(cur_id, scenarios):
    result = False
    l_scenario = json.loads(scenarios)
    for items in l_scenario:
        for values in items.values():
            if values == cur_id:
                result = True
                print(items)
    return result


def return_scenario_by_id(f_id, scenarios):
    for item in json.loads(scenarios):
        for key, value in item.items():
            if key == 'id':
                if value == f_id:
                    return item

