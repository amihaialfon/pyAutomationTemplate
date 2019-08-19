import requests


def send_post_message(path, message):
    r = requests.post(url=path, json=message)
    return r


def send_get_message(path, message):
    r = requests.get(url=path)
    return r
