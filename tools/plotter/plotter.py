from .server import Server


class Plotter:

    def __init__(self):
        self.server = Server(ip='localhost', port=8200)

    def plot(self, data):
        self.server.send_data(data)