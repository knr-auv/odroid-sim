from tools.position.position import Position


class TestPosition(Position):
    def __init__(self, config):
        Position.__init__(self, config)

    def _catch_samples(self):
        pass

    def _get_sample(self, sample):
        return 0
    