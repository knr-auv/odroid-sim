from .adafruitcontroller import AdafruitController
from .motortestcontroller import MotorTestController
from .simulationcontroller import SimulationController

controllers = {
    "AdaFruit": AdafruitController,
    "test": MotorTestController,
    "simulation": SimulationController
}


def get_motor_controller(config):
    return controllers[config.get("motors")](config)
