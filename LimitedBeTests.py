# to install pip in standalone run script:
# pip install -r wheelhouse/req.txt --no-index --find-links wheelhouse

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
    inJsonfileDict = ScenarioManager.get_scenario_file(scenario_name)
    inputTargetId = Finders.find_value_in_dict('id', inJsonfileDict)

    r = adapter.send_evaluation(message=scenario, method='post')
    assert r is not None, 'If r is None it means that no response where received from UUT'
    response_json = adapter.convert_to_dict(r.text)
    assert Finders.check_response(str(r)), 'Responses are not correct'  # Checks response for valid range.
    current_id = {'scenarioId': response_json['scenarioId']}
    print('Scenario is included in returned scenarios ' + str(current_id))
    response = None
    while response is None:
        print('Waiting evaluation unit response ' + str(datetime.now()) + '...')
        response = server.incoming_data
    logger.info(str(datetime.now()) + ' Response from BE: ' + (str(response)))
    finish_time = datetime.now()
    print(str(datetime.now()) + ' Response from BE: ' + (str(response)))
    print('Total time for response is: ' + str(finish_time - start_time))
    server.stop_server()
    outputTargetId = Finders.find_value_in_dict('id', response)
    print('Input Target Id: ' + str(inputTargetId) + ' | Output Target Id: ' + str(outputTargetId))
    #assert inputTargetId == outputTargetId, 'Target ID returned is not the same as what was sent!' # check if target id that return is the same
    interception_code = Finders.find_value_in_dict('interceptionFlag', response)
    print(interception_code)
    assert interception_code == True, 'interception Flag was returned in an unsuccessful state!'
    print('Test finish successfully!')


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
    test_post_result_evaluation_21395(scenario_name='translated_test.json')
    #test_post_result_evaluation_21395(scenario_name='EU_Input_SensorOutput_Example.json')
    #test_post_result_evaluation_21395(scenario_name='Minimal BE - Sample_Input_No_Eval_Data.json')
    #test_post_result_evaluation_21395(scenario_name='Minimal BE - Sample_Input_No_Eval_Data-with-policy.json')

    # test_delete_trajectory_21394()
