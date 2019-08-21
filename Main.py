from Utils import ScenarioManager
from Utils import Finders
from Utils import ConfigReader
from Utils.Logger import Logger
from Connection import RETB_Adapter

config = ConfigReader.get_config()
logger_setup = Logger.LoggerSetup(logger_name='logger', log_file='LogA.txt', log_dir=config['log_path'])
logger = Logger.get_loggerEx(logger_setup=logger_setup)
adapter = RETB_Adapter.RetbAdapter(logger=logger, config=config)

if __name__ == '__main__':
    logger.info('This is first test')
    reply_list = []
    # This is a test that checks scenario creation and consistency of all scenario attributes.
    scenario = ScenarioManager.get_scenario_file(scenario_name='scenario.json')
    r = adapter.send_scenarios(scenario, method='post')
    reply_list.append(r)
    if r is not None:
        response_json = adapter.convert_to_dict(r.text)
        if not Finders.check_response(str(r)):  # Checks response for valid range.
            assert (False, 'The response is out of correct range.')
        current_id = {'id': response_json['id']}
        r2 = adapter.send_scenarios(current_id, method='get')
        if not Finders.check_response(str(r2)):  # Checks response for valid range.
            assert (False, 'The response is out of correct range.')
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
    else:
        assert (False, 'The response is NoneType meaning none is there on the other end.')


def test_create_scenario():
    scenario = ScenarioManager.get_scenario_file()
    adapter.send_scenarios(scenario)
    print(scenario['id'])
