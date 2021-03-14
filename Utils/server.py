from datetime import datetime
from time import time
import flask
import threading
from Utils import ConfigReader, Finders
from Utils.Logger import Logger
from Connection import RETB_Adapter
import m2mLoad
app = flask.Flask(__name__)
config = ConfigReader.get_config()
ip = config['my_server_ip']
port = config['my_server_port']
incoming_data = None
logger_setup = Logger.LoggerSetup(logger_name='logger', log_file='LogA.txt', log_dir=config['my_log_path'])
logger = Logger.get_loggerEx(logger_setup=logger_setup)
adapter = RETB_Adapter.RetbAdapter(logger=logger, config=config)
count =0


def run_server():
    t = threading.Thread(target=app.run, args=(ip, port))
    t.start()
    print("started server")


def stop_server():
    import requests
    requests.post('http://' + ip + ":" + port + "/shutdown")


@app.route('/response', methods=['POST'])
def incoming_evaluation():
    global count
    count += 1
    print('response data was received!')
    logger.info('Testing is starting...')
    global incoming_data
    incoming_data = flask.request.json
    response = incoming_data

    return flask.Response('this is response')


def shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    run_server()

    import time

    time.sleep(2)
