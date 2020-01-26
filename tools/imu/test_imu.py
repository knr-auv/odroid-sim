from .imu import IMU


class TestIMU(IMU):

    def __init__(self, config):
        super(TestIMU, self).__init__(config)

    def _catch_samples(self):
        pass

    def _get_sample(self, sample):
        return 0
