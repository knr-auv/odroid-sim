import threading
import time
from variable import *



class KeySteeringThread(threading.Thread):
    def __init__(self, pid_thread, config):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.pid_thread = pid_thread
        self.last_time = time.time()

        # strojenie regulatorow #hardcoded
        pid_thread.roll_PID.setPIDCoefficients(4, 2, 2) # zahardkodowane narazie # nastawy  z testow
        pid_thread.pitch_PID.setPIDCoefficients(10, 2, 1)
        pid_thread.yaw_PID.setPIDCoefficients(0, 0, 0) # zera, bo horyzontalnymi silnikami sterujemy tylko padem

    def run(self):
        global motors_speed, motors_speed_pad, run_flag
        while True:
            pass
