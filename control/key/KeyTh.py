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
        config.get_client().set_orien([-10., -0.2, -5.], [0., 0., 0.])


        pid_thread.roll_PID.setPIDCoefficients(4, 2, 2)
        pid_thread.pitch_PID.setPIDCoefficients(10, 2, 1)
        pid_thread.yaw_PID.setPIDCoefficients(4, 3, 0)
        pid_thread.depth_PID.setPIDCoefficients(200, 0, 0)
        pid_thread.center_x_PID.setPIDCoefficients(0.5, 0, 0) # TODO: pid val
        pid_thread.center_y_PID.setPIDCoefficients(20, 0, 0) # TODO: pid val
        pid_thread.center_x_PID.turn_off() # Na poczatku uzywamy tylko yaw_PID
        pid_thread.center_y_PID.turn_off()
        pid_thread.depth_PID.setSetPoint(1)
        pid_thread.center_x_PID.setSetPoint(0)
        pid_thread.center_x_PID.setSetPoint(0)

        # pid_thread.depth_PID.setPIDCoefficients(10, 2, 1)
        # pid_thread.depth_PID.setSetPoint(1.5)

    def run(self):
        global motors_speed, motors_speed_pad, run_flag
        while True:
            p = int(input())
            motors_speed_pad[0] = 200
            motors_speed_pad[1] = 100