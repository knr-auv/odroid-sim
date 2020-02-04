from tools.position.position import Position


class SimulationPosition(Position):
    def __init__(self, config):
        Position.__init__(self, config)
        self.client = config.get_client()
        self.samples = None

    def _catch_samples(self):
        message = self.client.get_pos()
        if message is not None:
            self.samples = message

    def _get_sample(self, sample):
        if self.samples is None:
            return 0
        if sample == "roll":
            if self.samples['rot']['y'] > 180:
                return -360 + self.samples['rot']['y']
            return self.samples['rot']['z']
        elif sample == "pitch":
            if self.samples['rot']['x'] > 180:
                return 360-self.samples['rot']['x']
            return -self.samples['rot']['x']
        elif sample == "yaw":
            return self.samples['rot']['y']
        elif sample == "depth":
            return  -self.samples['pos']['y']
