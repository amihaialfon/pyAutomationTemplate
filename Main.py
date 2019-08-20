from Utils import ScenarioManager
from Utils import Finders
from Connection import rest_adapter as adapter
import json

if __name__ == '__main__':
    # This is a test that checks scenario creation and consistency of all scenario attributes.
    scenario = ScenarioManager.get_scenario_file()
    r = adapter.send_scenarios(scenario, method='post')
    response_json = json.loads(r.text)
    current_id = {'id': response_json['id']}
    r2 = adapter.send_scenarios(current_id, method='get')
    print(r2, r2.text)
    if Finders.find_id_in_scenario_get(response_json['id'], r2.text):
        print('Id found! yoohooo! ' + response_json['id'])
        scenario = ScenarioManager.update_scenario_id(scenario, 'id', response_json['id'])
        returned_scenario = Finders.return_scenario_by_id(response_json['id'], r2.text)
        if ScenarioManager.scenario_compare(scenario, returned_scenario):
            print('Scenarios are the same - PASS')
        else:
            print('Scenarios are different - FAIL')
    else:
        print('No match found!!! ERROR!')


def test_create_scenario():
    scenario = ScenarioManager.get_scenario_file()
    adapter.send_scenarios(scenario)
    print(scenario['id'])
