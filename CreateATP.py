import json
import Main
from Connection import RETB_Adapter
from Utils import ConfigReader
from Utils import Finders
from Utils import ScenarioManager
from Utils.Logger import Logger

config = ConfigReader.get_config()
logger_setup = Logger.LoggerSetup(logger_name='logger', log_file='LogA.txt', log_dir=config['my_log_path'])
logger = Logger.get_loggerEx(logger_setup=logger_setup)
adapter = RETB_Adapter.RetbAdapter(logger=logger, config=config)


def test_create_atp_scenario():
    Main.test_create_scenario_full_values_18937(scenario_name='#1 10 targets - Shilka.json')
    Main.test_create_scenario_full_values_18937(scenario_name='#2 280 targets - SR.json')
    Main.test_create_scenario_full_values_18937(scenario_name='#3 3080 targets - MR.json')
    Main.test_create_scenario_full_values_18937(scenario_name='#4 280 targets - 3 battery.json')
    Main.test_create_scenario_full_values_18937(scenario_name='#5 344 targets - 3 batteries.json')
    Main.test_create_scenario_full_values_18937(scenario_name='#6 2800 targets - SR opt.json')
    Main.test_create_scenario_full_values_18937(scenario_name='#7 10 targets - Shilka opt.json')
    Main.test_create_scenario_full_values_18937(scenario_name='#8 64 targets - 3 shilka.json')
