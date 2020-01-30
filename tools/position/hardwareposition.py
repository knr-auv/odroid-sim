from tools.position.position import Position
from tools.position.imu import IMUClass


class HardwarePosition(Position):

    def __init__(self, config):
        super().__init__(config)
        self.imu = IMUClass('roll', 'pitch', 'yaw', 'accel_proc_x', 'accel_proc_z', 'accel_proc_y','gyro_proc_z' ,'gyro_proc_x', 'gyro_raw_z')
        #self.depth_sensor = ...

    def _catch_samples(self):
        self.imu.catchSamples()
        #self.depth_sensor.catch_sample()

    def _get_sample(self, sample):
        return self.imu.getSample(sample)


