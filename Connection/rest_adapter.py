from Utils import ConfigReader
from Connection import rest_sender


config = ConfigReader.get_config()


def send_analysis(message):
    host_url = 'http://' + config['target_host'] + '/api/analysis'
    r = rest_sender.send_post_message(path = host_url, message=message)
    print(r)


def send_models(message):
    host_url = 'http://' + config['target_host'] + '/api/models'
    r = rest_sender.send_post_message(path=host_url, message=message)
    print(r)


def send_scenarios(message):
    host_url = 'http://' + config['target_host'] + '/api/scenarios'
    r = rest_sender.send_post_message(path=host_url, message=message)
    print(r)


def send_trajectories(message):
    host_url = 'http://' + config['target_host'] + '/api/trajectories'
    r = rest_sender.send_post_message(path=host_url, message=message)
    print(r)


if __name__ == '__main__':
    send_scenarios()
