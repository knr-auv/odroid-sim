import threading


class IMUThread(threading.Thread):
    """Thread class that reads IMU's input and prints it for testing reasons"""

    def __init__(self, imu):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.IMU = imu

    def run(self):
        # will start printing samples (maybe we could run it in another terminal)
        c = 0
        while True:
            self.IMU.catch_samples()
            # self.connObj.setDataFrame(self.IMU.get_sample())
            # self.IMU.printSamples(c % 50 == 0)
            c += 1

    def getIMU(self):
        return self.IMU

    def setIMU(self, imu):
        self.IMU = imu