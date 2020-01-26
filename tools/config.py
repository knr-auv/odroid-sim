import json


class Config(object):

    def __init__(self):
        self.data = None

    def load(self, read_file):
        self.data = json.load(read_file)

    def get(self, key):
        return self.data[key]

    def get_pid(self, key, part):
        return self.data["pid_"+key][part]
