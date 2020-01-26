

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

    def run_motor(self, motor_num, speed):
        return self._run_motor(motor_num, speed)

    def _run_motor(self, motor_num, speed):
        pass
