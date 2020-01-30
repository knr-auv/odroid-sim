

class MotorController:

    def __init__(self, config):
        self.frequency = config.get('frequency')
        self.min_pulse = 1.1
        self.mid_pulse = 1.5
        self.max_pulse = 1.9

        self.min_duty = 0
        self.mid_duty = 0
        self.max_duty = 0

        self.max_speed = 1000.
        self.min_speed = -1000.

    def initialize_all(self):
        return self._initialize_all()

    def _initialize_all(self):
        pass

    def run_motors(self, motors_speed):
        if len(motors_speed)==5:
            self._run_motors(motors_speed)

    def _run_motors(self, motors_speed):
        pass
