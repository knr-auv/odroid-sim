import threading


class POSThread(threading.Thread):
    """Thread class that reads IMU's input and prints it for testing reasons"""

    def __init__(self, imu):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.position_sensor = imu

    def run(self):
        # will start printing samples (maybe we could run it in another terminal)
        c = 0
        while True:
            self.position_sensor.catch_samples()
            # print (self.position_sensor.get_sample("roll"))
            # self.connObj.setDataFrame(self.IMU.get_sample())
            # self.IMU.printSamples(c % 50 == 0)
            c += 1

    def get_pos_sensor(self):
        return self.position_sensor

    def set_pos_sensor(self, pos):
        self.position_sensor = pos