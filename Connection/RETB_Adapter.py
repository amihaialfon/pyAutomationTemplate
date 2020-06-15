from Connection import RestSender
import json


class RetbAdapter():
    '''
    RETB Adapter is and adapter between automation framework and RETB backend.
    It contains all relevant pathes and methods that are used to create connection and dialog between
    automation framework and RETB backend.
    This class uses RestSender as an additional adapter to send REST requests, this is made in order to separate between
     technology and the logic.
    '''

    def __init__(self, logger, config):
        self.logger = logger,
        self.config = config

    def convert_to_dict(self, incoming):
        try:
            converted = json.loads(incoming)
            return converted
        except Exception as e:
            print(e)

    def send_analysis(self, message, type=''):
        if type == 'trajectories':
            type = 'trajectories'
        elif type == 'summary':
            type = 'query/summary'
        host_url = 'http://' + self.config['target_host'] + '/api/analysis' + '/' + type
        r = RestSender.send_post_message(path=host_url, message=message)
        print(r)
        return r

    def send_evaluation(self, message, method='post'):
        host_url = 'http://' + self.config['target_host'] + '/api/evaluation'
        print(host_url)
        if method == 'post':
            r = RestSender.send_post_message(path=host_url, message=message)
        elif method == 'get':
            host_url = + '/' + message
            r = RestSender.send_get_message(path=host_url)
        elif method == 'empty_post':
            r = RestSender.send_empty_post(path=host_url)
        print(r, r.text)
        return r

    def send_models(self, message):
        host_url = 'http://' + self.config['target_host'] + '/api/models'
        r = RestSender.send_get_message(path=host_url, message=message)
        print(r)
        return r

    def send_scenarios(self, message, type='', method='post'):
        host_url = 'http://' + self.config['target_host'] + '/api/scenarios'
        if type == 'projection':
            host_url += '?projection=id&projection=name'
        if type == 'upload':
            host_url += '10/upload'
        if method == 'post':
            r = RestSender.send_post_message(path=host_url, message=message)
        elif method == 'get':
            r = RestSender.send_get_message(path=host_url, message=message)
        elif method == 'put':
            host_url += '/' + type
            r = RestSender.send_put_message(path=host_url, message=message)
        print(r)
        return r

    def send_trajectories(self, scenarioid, message='', files='', method='post'):
        host_url = 'http://' + self.config['target_host'] + '/api/trajectories/upload?scenarioId=' + scenarioid
        print('host url: ' + host_url)
        if method == 'post_file':
            r = RestSender.send_post_file(path=host_url, files=files)
        if method == 'post':
            r = RestSender.send_post_message(path=host_url, message=message)
        elif method == 'get':
            r = RestSender.send_get_message(path=host_url)
        print(r)
        return r

    def delete_scenarios(self, message, method='DELETE'):
        host_url = 'http://' + self.config['target_host'] + '/api/scenarios/'
        r = RestSender.send_delete_message(path=host_url, message=message)
        print(r)
        return r

    def delete_trajectory(self, message, method='DELETE'):
        host_url = 'http://' + self.config['target_host'] + '/api/trajectory/'
        r = RestSender.send_delete_message(path=host_url, message=message)
        print(r)
        return r

    def start_optimization(self, message, method='post'):
        host_url = 'http://' + self.config['target_host'] + '/api/optimization'
        r = RestSender.send_post_message(path=host_url, message=message)
        print(r)
        return r