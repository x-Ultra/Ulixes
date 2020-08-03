import json


def get(name):
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data.get(name)


def cred_get(name):
    with open('credentials.json') as json_file:
        data = json.load(json_file)
        return data.get(name)


def hermes_get(name):
    with open('hermes.conf') as file:
        if name == "ID":
            return file.readlines()[0]
        elif name == "MY_IP":
            return file.readlines()[1]
