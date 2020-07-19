import json

def get(name):
	with open('config.json') as json_file:
	    data = json.load(json_file)
	    return data.get(name)