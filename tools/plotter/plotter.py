from .server import Server


class Plotter:

    def __init__(self):
        self.server = Server(ip='localhost', port=8200)
        self.data = {"depth": 0.0, "depth_r": 0.0, "roll": 0.0, "roll_r": 0.0, "pitch": 0.0, "pitch_r": 0.0, "yaw": 0.0,
                    "yaw_r": 0.0}

    def plot(self, depth=0.0, depth_r=0.0, roll=0.0, roll_r=0.0, pitch=0.0, pitch_r=0.0, yaw=0.0, yaw_r=0.0):
        self.data["depth"] = depth
        self.data["depth_r"] = depth_r
        self.data["roll"] = roll
        self.data["roll_r"] = roll_r
        self.data["pitch"] = pitch
        self.data["pitch_r"] = pitch_r
        self.data["yaw"] = yaw
        self.data["yaw"] = yaw_r
        self.server.send_data(self.data)