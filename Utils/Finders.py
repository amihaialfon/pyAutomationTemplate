import json


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
