# to install pip in standalone run script:
# pip install -r wheelhouse/req.txt --no-index --find-links wheelhouse

import json
import time
from datetime import datetime
from Utils import server
from Connection import Adapter
from Utils import ConfigReader
from Utils import Finders
from Utils import Manager
from Utils.Logger import Logger
import argparse

config = ConfigReader.get_config()
logger_setup = Logger.LoggerSetup(logger_name='logger', log_file='LogA.txt', log_dir=config['my_log_path'])
logger = Logger.get_loggerEx(logger_setup=logger_setup)
adapter = Adapter.Adapter(logger=logger, config=config)
count = 0
timeArray = []
parser = argparse.ArgumentParser()
parser.add_argument('--name', help=' name -> no need to type .json, default name is translated json')
args = parser.parse_args()


def post_file_and_wait_callback(name):
    #server.run_server()
    logger.info('This is a test that checks post evaluation at limited BE .' + name)
    name = Manager.get_file(name=name)
    in_json_file_dict = Manager.get_file(name)
    input_target_id = Finders.find_value_in_dict('id', in_json_file_dict)
    start_time = datetime.now()
    r = adapter.send_evaluation(message=name, method='post')
    assert r is not None, 'If r is None it means that no response where received from UUT'
    response_json = adapter.convert_to_dict(r.text)
    assert Finders.check_response(str(r)), 'Responses are not correct'  # Checks response for valid range.
    response = None
    once = True
    while response is None:
        if once:
            print('Waiting callback unit response ' + str(datetime.now()) + '...')
            print('To stop waiting and cancel the run press Crtl+C')
            once = False
        response = server.incoming_data
        finish_time = datetime.now()
    t = str(finish_time - start_time)
    (h, m, s) = t.split(':')
    result = float(h) * 3600 + float(m) * 60 + float(s)
    timeArray.append(result)
    print(result)
    logger.info(str(finish_time) + ' Response from BE: ' + (str(response)))
    print(str(finish_time) + ' Response from BE:')
    print(response)
    print('Total time for response is: ' + t)
    print('Test finish successfully! >>> ' + str(datetime.now()))


if __name__ == '__main__':
    logger.info('Limited BE Testing is starting...')
    print('Limited BE Testing is starting >>> ' + str(datetime.now()))
    server.run_server()
    startime = datetime.now()
    for i in range(0, 1):
        post_file_and_wait_callback(name='file.json')
        count += 1
    finishtime = datetime.now()
    print(timeArray)
    t = str(finishtime - startime)
    (h, m, s) = t.split(':')
    r = float(h) * 3600 + float(m) * 60 + float(s)
    print('Average response per post: '+str(sum(timeArray) / len(timeArray))+' seconds - for ' + str(count) + ' times, and total time for the whole run is: ' + str(r) + ' seconds ')
    server.stop_server()


    # test_delete_trajectory_21394()
