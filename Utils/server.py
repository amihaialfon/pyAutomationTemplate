import flask
import threading
from Utils import ConfigReader

app = flask.Flask(__name__)
config = ConfigReader.get_config()
ip = config['my_server_ip']
port = config['my_server_port']
incoming_data = None


def run_server():
    t = threading.Thread(target=app.run, args=(ip, port))
    t.start()
    print("started server")


def stop_server():
    import requests
    requests.post('http://' + ip + ":" + port + "/shutdown")


@app.route('/demo', methods=['POST'])
def incoming_evaluation():
    print('demo data received')
    global incoming_data
    incoming_data = flask.request.json
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
