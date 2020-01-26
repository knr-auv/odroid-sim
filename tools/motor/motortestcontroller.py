from .motorcontroller import MotorController
import os


class MotorTestController(MotorController):

    def __init__(self, config):
        super().__init__(config)

    def _initialize_all(self):
        print("Motor Initialization Test")

    def _run_motor(self, motor_num, speed):
        print("Motor {} Speed: {}".format(motor_num, speed))
