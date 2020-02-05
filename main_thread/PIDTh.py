import threading
import time
from tools.PID import PID
from tools.motor import get_motor_controller
from tools.Integrator import Integrator
from tools.printer.printer import Printer
from tools.plotter.plotter import Plotter
from variable import motors_speed_diff_pid, motors_speed_pad, PAD_STEERING_FLAG, READ_FLAG, RUN_FORWARD_VALUE


class PIDThread(threading.Thread):
    """Thread class that sets up all PID controllers and updates motors velocity after calculating difference
    between actual position and set_point position
    roll
    pitch
    yaw
    depth - not used yet because of lack of depth feedback in AUV
    velocity - not used because of lack of velocity feedback in AUV"""

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.roll_PID = PID()
        self.pitch_PID = PID()
        self.yaw_PID = PID()
        self.velocity_PID = PID()
        self.depth_PID = PID()
        # TODO: depth_PID object and things related to it

        self.center_x_PID = PID()
        self.center_x_diff = 0

        self.integrator = Integrator()
        # global motors_speed_diff_pid, motors_speed_pad
        global motors_speed_pad
        self.position_sensor = None
        self.roll_diff, self.pitch_diff, self.yaw_diff, self.velocity_diff, self.depth_diff = 0, 0, 0, 0, 0

        max_sum_output = 900.
        self.roll_PID.setMaxOutput(max_sum_output / 4)
        self.pitch_PID.setMaxOutput(max_sum_output / 4)
        self.yaw_PID.setMaxOutput(max_sum_output / 4)
        self.velocity_PID.setMaxOutput(max_sum_output / 4)
        self.depth_PID.setMaxOutput(max_sum_output / 4)

        self.pid_motors_speeds_update = [0, 0, 0, 0, 0]

        self.motors = get_motor_controller(config)
        self.motors.initialize_all()

        self.printer = Printer()
        self.plotter = Plotter()

    def run(self):
        now = time.time()
        while True:
            self.position_sensor.catch_samples()
            roll = self.position_sensor.get_sample('roll')
            pitch = self.position_sensor.get_sample('pitch')
            yaw = self.position_sensor.get_sample('yaw')
            depth = self.position_sensor.get_sample('depth')
            print("{} {} {}".format(roll, pitch, depth))
            self.plotter.plot(depth)
            #print(depth)
            self.roll_diff = self.roll_PID.update(roll)
            self.pitch_diff = self.pitch_PID.update(pitch)
            self.yaw_diff = self.yaw_PID.update(yaw)  # maybe try:  'gyro_raw_x' 'gro_proc_x'
            self.depth_diff = self.depth_PID.update(depth)
            # self.velocity_diff = self.velocity_PID.update(self.IMU.get_sample('vel_x'))

            # prints for testing reasons
            # print(self.roll_diff)
            # print(self.pitch_diff)
            # print(self.yaw_diff)
            self.roll_control()
            self.pitch_control()
            self.yaw_control()
            self.pad_control()
            self.center_x_control()
            self.depth_control()

            self.printer.set_roll(roll)
            self.printer.set_pitch(pitch)
            self.printer.set_yaw(yaw)
            # self.velocity_control()

            self.update_motors()
            self.printer.print_out()
            # print(time.time()-now)
            now = time.time()
            time.sleep(0.1)

    def roll_control(self):
        self.pid_motors_speeds_update[4] -= self.roll_diff
        self.pid_motors_speeds_update[2] += self.roll_diff

    def pitch_control(self):
        self.pid_motors_speeds_update[2] += self.pitch_diff  # * 2 / 3
        self.pid_motors_speeds_update[4] += self.pitch_diff  # * 2 / 3
        self.pid_motors_speeds_update[3] -= self.pitch_diff

    def yaw_control(self):
        global run_flag
        self.pid_motors_speeds_update[0] += self.yaw_diff
        self.pid_motors_speeds_update[1] -= self.yaw_diff
        if True:
            self.pid_motors_speeds_update[0] += RUN_FORWARD_VALUE
            self.pid_motors_speeds_update[1] += RUN_FORWARD_VALUE

    def pad_control(self):
        self.pid_motors_speeds_update[0] += motors_speed_pad[0]
        self.pid_motors_speeds_update[1] += motors_speed_pad[1]
        self.pid_motors_speeds_update[2] += motors_speed_pad[2]
        self.pid_motors_speeds_update[3] += motors_speed_pad[3]
        self.pid_motors_speeds_update[4] += motors_speed_pad[4]

    # not used yet
    def velocity_control(self):
        self.pid_motors_speeds_update[0] -= self.velocity_diff  # minusy bo silniki zamontowane odwrotnie?
        self.pid_motors_speeds_update[1] -= self.velocity_diff

    def center_x_control(self):
        self.pid_motors_speeds_update[0] -= self.center_x_diff
        self.pid_motors_speeds_update[1] += self.center_x_diff

    def depth_control(self):
        self.pid_motors_speeds_update[2] += 5 * self.depth_diff
        self.pid_motors_speeds_update[3] += 5 * self.depth_diff
        self.pid_motors_speeds_update[4] += 5 * self.depth_diff

    # method that updates motors velocity
    # you can pass velocity to pid_motors_speeds_update in cose to set the velocity on motors without PID controller
    # turned on
    def update_motors(self):
        # print(self.pid_motors_speeds_update)
        motors = self.motors.run_motors(self.pid_motors_speeds_update)
        self.printer.set_motors_value(motors)
        # print(motors)
        # motors_speed_diff_pid[:] = self.pid_motors_speeds_update[:]
        # print('Po przypisaniu:')
        # print(motors_speed_diff_pid)
        self.pid_motors_speeds_update = [0] * 5

    def get_position_sensor(self):
        return self.position_sensor

    def set_position_sensor(self, pos):
        self.position_sensor = pos
