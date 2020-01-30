from tools.position.position import Position


class SimulationPosition(Position):
    def __init__(self, config):
        super().__init__(config)
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
            return self.samples['rot']['x']
        elif sample == "pitch":
            return self.samples['rot']['y']
        elif sample == "yaw":
            return self.samples['rot']['z']
