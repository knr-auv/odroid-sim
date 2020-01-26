import threading
import time
import os
from tools.motor import get_motor_controller
from variable import motors_speed_diff_pid, run_flag


class MotorsControlThread(threading.Thread):
    """Thread class for setting and updating thrusters' velocity
    velocity is being given as value from -1000 to 1000 (pulse width)
    in comments name 'motors' and 'thrusters' are equal"""
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.motors = get_motor_controller(config)    # check freqency, maybe put slightly different one
        self.motors.initialize_all()   # thrusters need initialization process before running
        global motors_speed_diff_pid
        global run_flag
    def run(self):
        motors_speed = [0, 0, 0, 0, 0]
        while True:
            with self.lock:
                # prints velocity given to motors (thrusters)
                #print('Main:')
                #print(motors_speed_diff_pid)
                #print('---')
                #motors_speed = [0, 0, 0, 0, 0]
                #print("NA SILNIKI:")
                #print(motors_speed)    # comment

                #os.system('clear')
                for i in range(5):
                    motors_speed[i] += motors_speed_diff_pid[i]
                    #if (i ==0  or i ==1) and run_flag:
                    #    motors_speed[i] += RUN_FORWARD_VALUE  # previous version of "run" command execution - test new and del this
                    motors_speed_diff_pid[i] = 0
                    self.motors.run_motor(i, motors_speed[i])
                    #print("silnik {}, wypelnienie {}".format(i, motors_speed[i]))
                    motors_speed[i] = 0    # uncomment
                    #print("{}:{}".format(motors_names[i], motors_speed[i]), end=" ")    # comment
                #print(motors_speed)
            time.sleep(0.2)    # comment