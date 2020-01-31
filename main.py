import argparse

from variable import *
from main_thread import MotorsControlThread, POSThread, PIDThread
from control import get_control
from tools.position import get_pos
from tools.config import Config

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, type=str)
    args = parser.parse_args()

    config = Config()

    with open("configs/"+args.config, "r") as read_file:
        config.load(read_file)

    position_sensor = get_pos(config)

    motors_control_thread = MotorsControlThread(config)
    pos_thread = POSThread(position_sensor)
    pid_thread = PIDThread()
    pid_thread.set_position_sensor(position_sensor)
    control_thread = get_control(pid_thread, config)


    motors_control_thread.start()
    pos_thread.start()
    pid_thread.start()
    control_thread.start()
