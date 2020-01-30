from .motorcontroller import MotorController


class SimulationController(MotorController):

    def __init__(self, config):
        MotorController.__init__(config)
        self.client = config.get_client()

    def _initialize_all(self):
        print("Motor Initialization Test")

    def _run_motors(self, motors_speed):
        self.client.set_motors(motors_speed)
