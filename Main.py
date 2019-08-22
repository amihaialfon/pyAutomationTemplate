from Utils import ScenarioManager
from Utils import Finders
from Utils import ConfigReader
from Utils.Logger import Logger
from Connection import RETB_Adapter

config = ConfigReader.get_config()
logger_setup = Logger.LoggerSetup(logger_name='logger', log_file='LogA.txt', log_dir=config['log_path'])
logger = Logger.get_loggerEx(logger_setup=logger_setup)
adapter = RETB_Adapter.RetbAdapter(logger=logger, config=config)


def test_create_scenario():
    logger.info('This is a test that checks scenario creation and consistency of all scenario attributes.')
    scenario = ScenarioManager.get_scenario_file(scenario_name='scenario.json')
    r = adapter.send_scenarios(scenario, method='post')
    assert r is not None, 'If r is None it means that no response where received from UUT'
    response_json = adapter.convert_to_dict(r.text)
    assert Finders.check_response(str(r)), 'Responses are not correct'  # Checks response for valid range.
    current_id = {'id': response_json['id']}
    r2 = adapter.send_scenarios(current_id, method='get')
    assert Finders.check_response(str(r2))  # Checks response for valid range.
    assert Finders.find_id_in_scenario_get(response_json['id'],
                                           r2.text), 'Scenario is not among returned scenarios from UUT'
    print('Id found! yoohooo! ' + response_json['id'])
    scenario = ScenarioManager.update_scenario_id(scenario, 'id', response_json['id'])
    returned_scenario = Finders.return_scenario_by_id(response_json['id'], r2.text)
    assert ScenarioManager.scenario_compare(scenario, returned_scenario), 'Scenarios are different - FAIL'


if __name__ == '__main__':
    logger.info('This is first test')
    test_create_scenario()
