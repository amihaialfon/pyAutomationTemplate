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
    start_time = datetime.now()
    logger.info('This is a test that checks post evaluation at limited BE .' + scenario_name)
    scenario = ScenarioManager.get_scenario_file(scenario_name=scenario_name)
    r = adapter.send_evaluation(message=scenario, method='post')
    assert r is not None, 'If r is None it means that no response where received from UUT'
    response_json = adapter.convert_to_dict(r.text)
    assert Finders.check_response(str(r)), 'Responses are not correct'  # Checks response for valid range.
    current_id = {'scenarioId': response_json['scenarioId']}
    print('Scenario is included in returned scenarios' + str(current_id))
    response = None
    while response is None:
        print('Waiting evaluation unit response ' + str(datetime.now())+ ' ...')
        response = server.incoming_data
    logger.info(str(datetime.now())+ ' Response from BE: ' + (str(response)))
    print(str(datetime.now())+ ' Response from BE: ' + (str(response)))
    server.stop_server()
    # assert Finders.find_value_in_response(False, response), 'The value is within the response from the server!'
    print('Scenario is included in returned scenarios')

# @TODO add wait from EVAL unit post message

# def test_delete_trajectory_21394(scenario_id=None):
#     logger.info('This is a test that checks delete scenario.')
#     print('scenario ID: ' + scenario_id)
#     if scenario_id is None:
#         scenario_id = 'NotExistingID -'
#     message = {'scenarioId': scenario_id}
#     r = adapter.delete_trajectory(scenario_id)
#     assert Finders.check_response(str(r)), 'Response is valid range'  # Checks response for valid range.


if __name__ == '__main__':
    logger.info('Limited BE Testing is starting...')
    test_post_result_evaluation_21395(scenario_name='newLimitedBE_ScenarioDEV.json')
    # test_delete_trajectory_21394()
