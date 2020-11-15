import uuid
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


def ReturnJsonToSourceFile(jsonfile):
    logger.info('This script translate to response from M2M to json that can post ')
    scenario = ScenarioManager.get_scenario_file(scenario_name=jsonfile)
    data = {}

    with open('UIdata.json', 'w') as outfile:
        json.dump(data, outfile)




if __name__ == '__main__':
    logger.info('Script Testing is starting...')
    ReturnJsonToSourceFile(jsonfile='m2m_response.json')
