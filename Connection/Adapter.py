from Connection import RestSender
import json


class Adapter():

    def __init__(self, logger, config):
        self.logger = logger,
        self.config = config

    def convert_to_dict(self, incoming):
        try:
            converted = json.loads(incoming)
            return converted
        except Exception as e:
            print(e)

    def send(self, message, method='post', time_measured=False):
        host_url = 'http://' + self.config['target_host'] + '/api/'
        print(host_url)
        from time import time
        time_sent = time()
        if method == 'post':
            r = RestSender.send_post_message(path=host_url, message=message)
        elif method == 'get':
            host_url = + '/' + message
            r = RestSender.send_get_message(path=host_url)
        elif method == 'empty_post':
            r = RestSender.send_empty_post(path=host_url)
        print(r, r.text)
        time_delta = time() - time_sent
        if time_measured:
            return r, time_delta
        return r

    def delete(self, message, method='DELETE'):
        host_url = 'http://' + self.config['target_host'] + '/api/'
        r = RestSender.send_delete_message(path=host_url, message=message)
        print(r)
        return r

