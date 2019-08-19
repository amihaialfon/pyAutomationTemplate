import json


def find_id_in_scenario_get(id, scenarios):
    result = False
    l_scenario = json.loads(scenarios)
    for items in l_scenario:
        for values in items.values():
            if values == id:
                result=True
    return result

