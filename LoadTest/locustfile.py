# run service: locust --host=http://localhost:8089/
from locust import Locust, HttpLocust, TaskSet, task, between
import json

target_host = "http://dev.retb.cv.rafael:5080"
sourcesJson = "./Sources/"

analysis = "/api/analysis/query/summary"
evaluation = '/api/evaluation/'
send_scenarios = '/api/scenarios'
send_trajectories = "/api/trajectories/upload?scenarioId=" + "e0989257-8f57-4a67-8889-eafedacaae1f"
delete_scenarios = '/api/scenarios/'
optimization = '/api/optimization'


# send_models = '/api/models'


class MyTaskSet(TaskSet):
    # @task
    # def send_assets_analysis(self):
    #     with open(sourcesJson + "assets.json") as json_file:
    #         data = json.load(json_file)
    #         reply = self.client.post(analysis, json=data)
    #         print(reply)
    #         print(reply.text)

    @task
    def send_evaluation(self):
        with open(sourcesJson + "translated_test.json") as json_file:
            data = json.load(json_file)
            reply = self.client.post(evaluation, json=data)
            print(reply)
            print(reply.text)

    # @task
    # def send_scenarios(self):
    #     with open(sourcesJson + "scenario_full_values.json") as json_file:
    #         data = json.load(json_file)
    #         reply = self.client.post(send_scenarios, json=data)
    #         print(reply)
    #         print(reply.text)

    # @task
    # def send_trajectories(self):
    #     import os
    #     root = os.path.dirname(__file__)
    #     filename = (root + '\\Sources\\' + "trajectoriesB.json")
    #     files = {'trajectoriesFile': open(filename, 'rb')}
    #     print(filename)
    #     reply = self.client.post(send_trajectories, files=files)
    #     print(reply)
    #     print(reply.text)

    # @task
    # def send_optimization(self):
    #     with open("./Sources/" + "trajectories.json") as json_file:
    #         data = json.load(json_file)
    #         reply = self.client.post(send_trajectories, json=data)
    #         print(reply)


class MyLocust(HttpLocust):
    task_set = MyTaskSet
    wait_time = between(1, 1)  # seconds
