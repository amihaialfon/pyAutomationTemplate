import json
from datetime import datetime
from Utils import server
from Connection import RETB_Adapter
from Utils import ConfigReader
from Utils import Finders
from Utils import ScenarioManager
from Utils.Logger import Logger

config = ConfigReader.get_config()
logger_setup = Logger.LoggerSetup(logger_name='logger', log_file='LogA.txt', log_dir=config['my_log_path'])
logger = Logger.get_loggerEx(logger_setup=logger_setup)
adapter = RETB_Adapter.RetbAdapter(logger=logger, config=config)
scenario_id = 'NotExistingID -'


def test_post_result_evaluation_21395(scenario_name):
    server.run_server()
    logger.info('This is a test that checks post evaluation at limited BE .' + scenario_name)
    scenario = ScenarioManager.get_scenario_file(scenario_name=scenario_name)
    start_time = datetime.now()
    r = adapter.send_evaluation(scenario, method='post')
    assert r is not None, 'If r is None it means that no response where received from UUT'
    response_json = adapter.convert_to_dict(r.text)
    assert Finders.check_response(str(r)), 'Responses are not correct'  # Checks response for valid range.
    current_id = {'id': response_json['id']}
    r2 = adapter.send_evaluation(scenario, method='post')
    assert Finders.check_response(str(r2)), 'Response is valid range'  # Checks response for valid range.
    assert Finders.find_id_in_scenario_get(response_json['id'],
                                           r2.text), 'Scenario is not among returned scenarios from UUT'
    print('Scenario is included in returned scenarios')
    resonse = None
    while resonse is None:
        print('waiting evaluation unit response')
        resonse = server.incoming_data
    print(resonse)
    server.stop_server()
    assert resonse == '123', "the data is wrong"

# @TODO add wait from EVAL unit post message


def test_delete_trajectory_21394(scenario_id=None, mode=False):
    logger.info('This is a test that checks delete scenario.')
    print('scenario ID: ' + scenario_id)
    if scenario_id is None:
        scenario_id = 'NotExistingID -'
    message = {'scenarioId': scenario_id}
    r = adapter.delete_trajectory(scenario_id)
    assert Finders.check_response(str(r)), 'Response is valid range'  # Checks response for valid range.


if __name__ == '__main__':
    logger.info('Limited BE Testing is starting...')
    test_post_result_evaluation_21395(scenario_name='newElevation.json')
    # test_delete_trajectory_21394()
