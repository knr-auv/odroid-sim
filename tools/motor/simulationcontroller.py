from .motorcontroller import MotorController


class SimulationController(MotorController):

    def __init__(self, config):
        MotorController.__init__(self, config)
        self.client = config.get_client()

    def _initialize_all(self):
        print("Motor Initialization Test")

    def _run_motors(self, motors_speed):
        if len(motors_speed) == 5:
            for i in range(5):
                if motors_speed[i] > 1000:
                    motors_speed[i] = 1000
                elif motors_speed[i] < -1000:
                    motors_speed[i] = -1000
            self.client.set_motors(motors_speed)
