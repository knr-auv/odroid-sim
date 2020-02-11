from .motorcontroller import MotorController


class SimulationController(MotorController):

    def __init__(self, config):
        MotorController.__init__(self, config)
        self.client = config.get_client()

    def _initialize_all(self):
        print("Motor Simulation Initialization Test")

    def _run_motors(self, motors_data):
        if len(motors_data) == 5:
            self.client.motors_data["FL"] = -motors_data[4] / 1000
            self.client.motors_data["FR"] = -motors_data[2] / 1000
            self.client.motors_data["ML"] = motors_data[0] / 1000
            self.client.motors_data["MR"] = motors_data[1] / 1000
            self.client.motors_data["B"] = motors_data[3] / 1000
        self.client.set_motors()