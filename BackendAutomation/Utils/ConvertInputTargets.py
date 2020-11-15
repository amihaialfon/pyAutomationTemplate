import json
import os
import copy
from datetime import datetime
from Connection import RETB_Adapter
from Utils import ConfigReader
from Utils import Finders
from Utils import ScenarioManager
from Utils.Logger import Logger

config = ConfigReader.get_config()
logger_setup = Logger.LoggerSetup(logger_name='logger', log_file='LogA.txt', log_dir=config['my_log_path'])
logger = Logger.get_loggerEx(logger_setup=logger_setup)
adapter = RETB_Adapter.RetbAdapter(logger=logger, config=config)


def get_input_file(inputFile):
    try:
        root = os.path.dirname(__file__)
        root = root.rstrip('\\Utils')
        filename = (root + '\\Sources\\Targets\\' + inputFile)
        with open(filename, 'r') as f:
            file = json.load(f)
            print("File was load..")
            return file
    except IOError as e:
        print(e)


def findKeyinJson(to_find, file):
    for key, value in file.items():
        if key == to_find:
            return value
        elif type(value) == dict:
            for in_key, in_value in value.items():
                if in_key == to_find:
                    return in_value
                elif type(in_value) == dict:
                    for iin_key, iin_value in in_value.items():
                        if iin_key == to_find:
                            return iin_value

def replacePartinJson(to_find, file, part):
    for key, value in file.items():
        if key == to_find:
            value = part
            print(file.items())
            print(value)
            return file
        elif type(value) == dict:
            for in_key, in_value in value.items():
                if in_key == to_find:
                    in_value = part
                    print(value.items())
                    print(in_value)
                    return file
                elif type(in_value) == dict:
                    for iin_key, iin_value in in_value.items():
                        if iin_key == to_find:
                            iin_value = part
                            print(in_value.items())
                            print(iin_value)
                            return file


def convinputfile(srcFileName):
    inputjsonFile = get_input_file(srcFileName)
    targetsInput = get_input_file("targetsInput.json")
    relevantpart = replacePartinJson('target', inputjsonFile, targetsInput)
    #print (relevantpart)
    return


if __name__ == '__main__':
    print('Convert Target file...')
    convinputfile(srcFileName='alexInput.json')
