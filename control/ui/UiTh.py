import threading
import time
import pickle
from variable import motors_speed, motors_speed_pad, run_flag, IP_ADDRESS_2, PAD_PORT, SAVE_FLAG, MOVES_FILE


class UIThread(threading.Thread):
    """Thread class that is terminal's UI for setting PIDs, primitive steering by commands """
    def __init__(self, pid_thread, config):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.prev_speed = motors_speed[:]
        self.motors_wait_thread = MotorsWaitThread(0, [])
        self.pid_thread = pid_thread

    def run(self):
        global motors_speed, motors_names, run_flag

        while True:
            cmd = input()
            args = cmd.split(' ')
            print(args)

            with self.lock:
                if len(args) == 3:
                    self.prev_speed[:] = motors_speed[:]

                if args[0] == "s":
                    print("Stopping all motors")
                    motors_speed = [0] * 5
                    self.motors_wait_thread.prev_speed[:] = [0] * 5

                for name in motors_names:
                    if args[0] == name and args[1]:
                        motors_speed[motors_names.index(name)] = int(args[1])
                        print("Changing {} speed to {}".format(name, int(args[1])))

                if args[0] == 'h':
                    motors_speed[0] = int(args[1])
                    motors_speed[1] = int(args[1])
                    print("Changing H motors speeds to {}".format(int(args[1])))

                if args[0] == 'v':
                    motors_speed[2] = int(args[1])
                    motors_speed[3] = int(args[1])
                    motors_speed[4] = int(args[1])
                    print("Changing V motors speeds to {}".format(int(args[1])))

                if args[0] == 'vlr':
                    motors_speed[2] = int(args[1])
                    motors_speed[4] = int(args[1])
                    print("Changing V l&r motors speeds to {}".format(int(args[1])))

                if args[0] == "pid":
                    var = args[1]
                    Kp, Ki, Kd = float(args[2]), float(args[3]), float(args[4])
                    if var == 'x':
                        pid_thread.roll_PID.setPIDCoefficients(Kp, Ki, Kd)

                    if var == 'y':
                        pid_thread.pitch_PID.setPIDCoefficients(Kp, Ki, Kd)

                    if var == 'z':
                        pid_thread.yaw_PID.setPIDCoefficients(Kp, Ki, Kd)

                    if var == 'v':
                        pid_thread.velocity_PID.setPIDCoefficients(Kp, Ki, Kd)

                if args[0] == "vel":
                    pid_thread.velocity_PID.setSetPoint(args[1])

                if args[0] == "run":
                    run_flag = True
                if args[0] == 'stop':
                    run_flag = False

                #elif len(args) != 3:
                    #motor_wait_thread = MotorsWaitThread(float(args[2]), self.prev_speed)
                    #motor_wait_thread.start()
