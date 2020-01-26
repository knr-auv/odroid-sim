from .adafruitcontroller import AdafruitController
from .motortestcontroller import MotorTestController

controllers = {
    "AdaFruit": AdafruitController,
    "test": MotorTestController
}


def get_motor_controller(config):
    return controllers[config.get("motors")](config)
