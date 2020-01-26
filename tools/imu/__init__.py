from .imu_um7 import UM7IMU
from .test_imu import TestIMU

imus = {
    "UM7": UM7IMU,
    "test": TestIMU
}


def get_imu(config):
    return imus[config.get("imu")](config)
