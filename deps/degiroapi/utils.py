import json


def pretty_json(data):
    return json.dumps(data, indent=4, sort_keys=True)
