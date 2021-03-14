import json
from selenium.webdriver import Chrome
from Utils import ConfigReader
from Utils import Finders
from Utils import Manager
from Utils.Logger import Logger
from Connection import Adapter

config = ConfigReader.get_config()
logger_setup = Logger.LoggerSetup(logger_name='logger', log_file='LogA.txt', log_dir=config['my_log_path'])
logger = Logger.get_loggerEx(logger_setup=logger_setup)
adapter = Adapter.Adapter(logger=logger, config=config)
browser = Chrome()
browser.get('https://www.google.com')
xpath = browser.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input')

def test():

    print('startting fill at: ' + browser.title)
    xpath.send_keys("testing")


if __name__ == '__main__':
    logger.info('Testing is starting...')
    test()
    browser.close()




