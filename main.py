import argparse

from variable import *
from main_thread import MotorsControlThread, POSThread, PIDThread
from control import get_control
from tools.position import get_pos
from tools.config import Config
import logging
from concurrent.futures import ThreadPoolExecutor
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    #im sick of starting main with arguments...
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=False, type=str)
    args = parser.parse_args()
    config = Config()
    if args.config == None:
        with open("configs/GUI.json", "r") as read_file:
            config.load(read_file)
    else:
        with open("configs/"+args.config, "r") as read_file:
            config.load(read_file)

    position_sensor = get_pos(config)
    pid_thread = PIDThread(config)
    pid_thread.set_position_sensor(position_sensor)
    control_thread = get_control(pid_thread, config)
    if config.get("control")=="GUI":
        control_thread.start()
    else:
        control_thread.start()
        pid_thread.start()
    
    
