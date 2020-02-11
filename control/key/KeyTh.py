import threading
import time
from variable import *



class KeySteeringThread(threading.Thread):
    def __init__(self, pid_thread, config):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.pid_thread = pid_thread
        self.last_time = time.time()

        # strojenie regulatorow #hardcoded potem będą w configach
        pid_thread.roll_PID.setPIDCoefficients(4, 2, 2)
        pid_thread.pitch_PID.setPIDCoefficients(10, 2, 1)
        pid_thread.yaw_PID.setPIDCoefficients(4, 3, 0)
        pid_thread.yaw_PID.setSetPoint(30)

        # pid_thread.depth_PID.setPIDCoefficients(10, 2, 1)
        # pid_thread.depth_PID.setSetPoint(1.5)

    def run(self):
        global motors_speed, motors_speed_pad, run_flag
        while True:
            pass
            # motors_speed_pad[0] = 200
            # motors_speed_pad[1] = 200
