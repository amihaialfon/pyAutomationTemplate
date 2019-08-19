from Utils import ConfigReader
from Connection import rest_sender

config = ConfigReader.get_config()


def send_analysis(message):
    host_url = 'http://' + config['target_host'] + '/api/analysis'
    r = rest_sender.send_post_message(path=host_url, message=message)
    print(r)
    return r


def send_models(message):
    host_url = 'http://' + config['target_host'] + '/api/models'
    r = rest_sender.send_post_message(path=host_url, message=message)
    print(r)
    return r


def send_scenarios(message, method='post'):
    host_url = 'http://' + config['target_host'] + '/api/scenarios'
    if method == 'post':
        r = rest_sender.send_post_message(path=host_url, message=message)
    elif method == 'get':
        #temp = host_url+'/'+message
        #print(temp)
        r = rest_sender.send_get_message(path=host_url, message=message)
    print(r)
    return r


def send_trajectories(message):
    host_url = 'http://' + config['target_host'] + '/api/trajectories'
    r = rest_sender.send_post_message(path=host_url, message=message)
    print(r)
    return r


if __name__ == '__main__':
    send_scenarios()
