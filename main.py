import argparse

from variable import *
from main_thread import MotorsControlThread, IMUThread, PIDThread
from control import get_control
from tools.imu import get_imu
from tools.config import Config

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, type=str)
    args = parser.parse_args()

    config = Config()

    with open("configs/"+args.config, "r") as read_file:
        config.load(read_file)

    imu = get_imu(config)

    motors_control_thread = MotorsControlThread(config)
    imu_thread = IMUThread(imu)
    pid_thread = PIDThread()
    pid_thread.setIMU(imu)
    control_thread = get_control(pid_thread, config)


    motors_control_thread.start()
    imu_thread.start()
    pid_thread.start()
    control_thread.start()
