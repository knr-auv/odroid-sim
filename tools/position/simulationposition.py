from tools.position.position import Position


class SimulationPosition(Position):
    def __init__(self, config):
        Position.__init__(self, config)
        self.client = config.get_client()
        self.samples = None
        self.licznik = 0
        self.mianownik = 0

    def _catch_samples(self):
        message = self.client.get_sens()
        self.mianownik += 1
        if message is not None:
            self.samples = message

    def _get_sample(self, sample):
        if self.samples is None:
            return 0
        if sample == "roll":
            if self.samples['gyro']['z'] > 180:
                return -360 + self.samples['gyro']['z']
            elif self.samples['gyro']['z'] < -180:
                return 360 + self.samples['gyro']['z']
            return self.samples['gyro']['z']
        elif sample == "pitch":
            if self.samples['gyro']['x'] > 180:
                return 360 - self.samples['gyro']['x']
            if self.samples['gyro']['x'] < -180:
                return -360 - self.samples['gyro']['x']
            return -self.samples['gyro']['x']
        elif sample == "yaw":
            return self.samples['gyro']['y']
        elif sample == "depth":
            return  self.samples["baro"]["pressure"]/9800
