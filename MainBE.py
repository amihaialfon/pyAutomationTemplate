import json
from flask import Flask
import threading
from Connection import Adapter
from Utils import ConfigReader
from Utils import Finders
from Utils import Manager
from Utils.Logger import Logger

config = ConfigReader.get_config()
logger_setup = Logger.LoggerSetup(logger_name='logger', log_file='LogA.txt', log_dir=config['my_log_path'])
logger = Logger.get_loggerEx(logger_setup=logger_setup)
adapter = Adapter.Adapter(logger=logger, config=config)


def first_test():
    logger.info('This is a sample test!')
    name = Manager.get_file(name='empty_values.json')
    r = adapter.send(name, method='post')
    assert r is not None, 'If r is None it means that no response where received from UUT'
    response_json = adapter.convert_to_dict(r.text)
    assert Finders.check_response(str(r)), 'Responses are not correct'  # Checks response for valid range.
    current_id = {'id': response_json['id']}
    r2 = adapter.send(current_id, method='get')
    assert Finders.check_response(str(r2))  # Checks response for valid range.



if __name__ == '__main__':
    logger.info('Testing is starting...')
    first_test(name='retranslate_file.json')

