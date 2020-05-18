import flask
import threading
from Utils import ConfigReader

app = flask.Flask(__name__)
config = ConfigReader.get_config()
ip = config['my_server_ip']
port = config['my_server_port']
t = threading.Thread(target=app.run, args=(ip, port))


def run_server():
    t.start()
    print("started server")


def stop_server():
    if t is not None:
        print('terminating server')
        t.join()
    else:
        print("Server is not running")


@app.route('/demo', methods=['POST'])
def demo():
    print('demo data received')
    x = flask.request.json
    print(x)
    return flask.Response('this is response')


if __name__ == '__main__':
    run_server()
