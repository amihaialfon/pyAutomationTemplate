import requests


def send_post_file(path, files):
    try:
        files = {'trajectoriesFile': open(files, 'rb')}
        r = requests.post(url=path, files=files)
        return r
    except requests.exceptions.RequestException as e:
        print(e)


def send_post_message(path, message):
    try:
        r = requests.post(url=path, json=message)
        return r
    except requests.exceptions.RequestException as e:
        print(e)


def send_empty_post(path):
    try:
        r = requests.post(url=path)
        return r
    except requests.exceptions.RequestException as e:
        print(e)


def send_get_message(path, message):
    try:
        r = requests.get(url=path)
        return r
    except requests.exceptions.RequestException as e:
        print(e)


def send_delete_message(path, message):
    try:
        # r = requests.delete(url=path, json=message)
        r = requests.request("DELETE", path+'/'+message)
        return r
    except requests.exceptions.RequestException as e:
        print(e)


def send_put_message(path, message):
    try:
        r = requests.put(url=path)
        return r
    except requests.exceptions.RequestException as e:
        print(e)
