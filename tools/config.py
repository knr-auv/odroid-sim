import json
from .simulationclient.simulationclient import SimulationClient


class Config(object):

    def __init__(self):
        self.data = None
        self.client = None

    def load(self, read_file):
        self.data = json.load(read_file)
        if(self.data["mode"]=="simulation"):
            self.client = SimulationClient()

    def get(self, key):
        return self.data[key]

    def get_pid(self, key, part):
        return self.data["pid_"+key][part]

    def get_client(self):
        return self.client

