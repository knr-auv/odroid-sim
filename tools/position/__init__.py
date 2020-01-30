from .hardwareposition import HardwarePosition
from .testposition import TestPosition
from .simulationposition import SimulationPosition

pos = {
    "hardware": HardwarePosition,
    "test": TestPosition,
    "simulation": SimulationPosition
}

def get_pos(config):
    return pos[config.get("pos")](config)