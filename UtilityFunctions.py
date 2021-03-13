import json
import os


def read_json(json_object):
    if os.path.exists(json_object):
        with open(json_object, 'rb') as file:
            json_object = file.read()
    return json.loads(json_object)