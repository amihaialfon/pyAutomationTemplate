from Utils import ScenarioManager
from Utils import Finders
from Utils import ConfigReader
from Utils.Logger import Logger
from Connection import RETB_Adapter
import json
import socket
import pytest

config = ConfigReader.get_config()
logger_setup = Logger.LoggerSetup(logger_name='logger', log_file='LogA.txt', log_dir=config['my_log_path'])
logger = Logger.get_loggerEx(logger_setup=logger_setup)
adapter = RETB_Adapter.RetbAdapter(logger=logger, config=config)


def test_create_scenario_empty_values_18359():
    logger.info('This is a test that checks scenario creation and consistency of all scenario attributes.')
    scenario = ScenarioManager.get_scenario_file(scenario_name='scenario_empty_values.json')
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


def test_create_scenario_full_values_18937(scenario_name):
    logger.info('This is a test that checks post evaluation.' + scenario_name)
    # scenario = ScenarioManager.get_scenario_file(scenario_name='scenario_full_values.json')
    scenario = ScenarioManager.get_scenario_file(scenario_name=scenario_name)
    r = adapter.send_scenarios(scenario, method='post')
    assert r is not None, 'If r is None it means that no response where received from UUT'
    response_json = adapter.convert_to_dict(r.text)
    assert Finders.check_response(str(r)), 'Responses are not correct'  # Checks response for valid range.
    current_id = {'id': response_json['id']}
    r2 = adapter.send_scenarios(current_id, method='get')
    assert Finders.check_response(str(r2)), 'Response is valid range'  # Checks response for valid range.
    assert Finders.find_id_in_scenario_get(response_json['id'],
                                           r2.text), 'Scenario is not among returned scenarios from UUT'
    print('Scenario is included in returned scenarios')
    scenario = ScenarioManager.update_scenario_id(scenario, 'id', response_json['id'])
    returned_scenario = Finders.return_scenario_by_id(response_json['id'], r2.text)
    assert ScenarioManager.scenario_compare(scenario, returned_scenario), 'Scenarios are different - FAIL'
    return response_json['id']


def test_analysis_18938(evaluation_id=None, mode=False):
    logger.info('This test is checking analysis')
    if evaluation_id is None:
        evaluation_id = 'bc593ca2-11b8-4c0d-addf-7aed32d21a90'
    print(evaluation_id)
    message = {'evaluationId': evaluation_id}
    asset = ScenarioManager.get_scenario_file(scenario_name='assets.json')
    message.update(asset)
    print(message)
    r = adapter.send_analysis(message=message, type='summary')
    assert Finders.check_response(str(r)), 'Response is valid range'  # Checks response for valid range.
    print(r, r.text)


def test_result_evaluation_18939(scenario_id=None, mode=False):
    logger.info('This test is checking evaluation')
    if scenario_id is None:
        scenario_id = 'NotExistingID -'
    message = {'scenarioId': scenario_id}
    r = adapter.send_evaluation(message=message)
    temp = 'statusCode":500,"error":"Internal Server Error","message":"Scenario id NotExistingID - doesn\'t exist'
    if mode:
        assert Finders.check_response(str(r)), 'Responses are not correct'  # Checks response for valid range.
        r_dict = json.loads(r.text)
        print(r_dict['id'])
        return r_dict['id']
    if not mode:
        assert temp in r.text


def test_upload_trajectory_18940(scenario_id=None):
    logger.info('This is a test that checks uploaded Trajectories.')
    scenario = ScenarioManager.get_scenario_file(scenario_name='scenario_full_values.json')
    r = adapter.send_scenarios(scenario, method='post')
    assert r is not None, 'If r is None it means that no response where received from UUT'
    response_json = adapter.convert_to_dict(r.text)
    assert Finders.check_response(str(r)), 'Responses are not correct'  # Checks response for valid range.
    current_id = {'id': response_json['id']}
    r2 = adapter.send_scenarios(current_id, method='get')
    assert Finders.check_response(str(r2))  # Checks response for valid range.
    print('response is valid range')
    assert Finders.find_id_in_scenario_get(response_json['id'],
                                           r2.text), 'Scenario is not among returned scenarios from UUT'
    print('Scenario is included in returned scenarios')
    if scenario_id is None:
        scenario_id = (response_json['id'])
    print(scenario_id)
    trajectory_path = ScenarioManager.get_file_path(in_filename='trajectories.json')
    r3 = adapter.send_trajectories(scenario_id, files=trajectory_path, method='post_file')
    print('send trajectory:' + str(r3))
    assert r3 is not None, 'If r is None it means that no response where received from UUT'
    # response_json = adapter.convert_to_dict(r3.text)
    assert Finders.check_response(r3), 'Responses are not correct:' + str(r3)  # Checks response for valid range.
    print(r3.text)


def test_delete_scenario_19332(scenario_id=None, mode=False):
    logger.info('This is a test that checks delete scenario.')
    print('scenario ID: ' + scenario_id)
    if scenario_id is None:
        scenario_id = 'NotExistingID -'
    message = {'scenarioId': scenario_id}
    r = adapter.delete_scenarios(scenario_id)
    assert Finders.check_response(str(r)), 'Response is valid range'  # Checks response for valid range.


def test_full_analyze_18941():
    logger.info('This is a test that check full analyze scenario')
    scenarioId = test_create_scenario_full_values_18937(scenario_name='scenario_50_deployments.json')
    print('scenario ID: ' + scenarioId)
    test_upload_trajectory_18940(scenario_id=scenarioId)
    eval_id = test_result_evaluation_18939(scenario_id=scenarioId, mode=True)
    test_analysis_18938(eval_id)
    test_delete_scenario_19332(scenario_id=scenarioId)


# def test_optimization_analyze_19775(scenario_id=None, mode=False):  # need to check
#     logger.info('This is a test that check automatic optimization analyze scenario')
#     if scenario_id is None:
#         scenario_id = 'NotExistingID -'
#     message = {'scenarioId': scenario_id}
#     r = adapter.start_optimization(message=message)
#     temp = 'statusCode":500,"error":"Internal Server Error","message":"Scenario id NotExistingID - doesn\'t exist'
#     if mode:
#         assert Finders.check_response(str(r)), 'Responses are not correct'  # Checks response for valid range.
#         r_dict = json.loads(r.text)
#         print(r_dict['id'])
#         return r_dict['id']
#     if not mode:
#         assert temp in r.text


if __name__ == '__main__':
#    logger.info('Testing is starting...')
#   test_upload_trajectory_18940(scenario_id="bc593ca2-11b8-4c0d-addf-7aed32d21a90")
#    test_analysis_18938()
#    test_full_analyze_18941()
#   test_upload_trajectory_18940()
#   test_result_evaluation_18939()
#   test_analysis_18938()
#   test_create_scenario_full_values_18937(scenario_name='scenario_50_deployments.json')
#   # test_create_scenario_full_values_18937(scenario_name='scenario_full_Test_Lot_Asset_Deploy.json')
#   test_create_scenario_full_values_18937(scenario_name='scenario_full_values.json')
#   test_create_scenario_empty_values_18359()
#   test_full_analyze_18941()
    test_create_scenario_full_values_18937(scenario_name='#1 10 targets - Shilka.json')
    test_create_scenario_full_values_18937(scenario_name='#2 280 targets - SR.json')
    test_create_scenario_full_values_18937(scenario_name='#3 3080 targets - MR.json')
    test_create_scenario_full_values_18937(scenario_name='#4 280 targets - 3 battery.json')
    test_create_scenario_full_values_18937(scenario_name='#5 344 targets - 3 batteries.json')
    test_create_scenario_full_values_18937(scenario_name='#6 2800 targets - SR opt.json')
    test_create_scenario_full_values_18937(scenario_name='#7 10 targets - Shilka opt.json')
    test_create_scenario_full_values_18937(scenario_name='#8 64 targets - 3 shilka.json')
