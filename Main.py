from Utils import ScenarioReader
from Utils import Finders
from Connection import rest_adapter as adapter
import json

if __name__ == '__main__':
    scenario = ScenarioReader.get_scenario_file()
    r = adapter.send_scenarios(scenario, method='post')
    print(r.text)
    response_json = json.loads(r.text)
    current_id = {'id': response_json['id']}
    r2 = adapter.send_scenarios(current_id, method='get')
    print(r2, r2.text)
    print(r2.text)
    if Finders.find_id_in_scenario_get(response_json['id'], r2.text):
        print('Id found! yoohooo! ' + response_json['id'])
    else:
        print('No match found!!! ERROR!')


def test_create_scenario():
    scenario = ScenarioReader.get_scenario_file()
    adapter.send_scenarios(scenario)
    print(scenario['id'])
