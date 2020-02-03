from .motorcontroller import MotorController
import os


class MotorTestController(MotorController):

    def __init__(self, config):
        MotorController.__init__(self, config)

    def _initialize_all(self):
        print("Motor Initialization Test")

    def _run_motor(self, motor_num, speed):
        pass

    def _run_motors(self, motors_speed):
        for i in range(5):
            self._run_motor(i, motors_speed[i])
