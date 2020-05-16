import threading
import logging
import time, random
from tools.PID import PID
from tools.motor import get_motor_controller
from tools.Integrator import Integrator
from tools.printer.printer import Printer
from tools.plotter.plotter import Plotter
from variable import motors_speed_diff_pid, motors_speed_pad, PAD_STEERING_FLAG, READ_FLAG, RUN_FORWARD_VALUE, motors_speed


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

        #gui stuff
        self.active = True
        self.isActive = False
        self.m = [0,0,0,0,0]
        
        # TODO: depth_PID object and things related to it

        self.center_x_PID = PID()
        self.center_x_diff = 0
        self.integrator = Integrator()
        # global motors_speed_diff_pid, motors_speed_pad
        global motors_speed_pad
        self.position_sensor = None
        self.roll_diff, self.pitch_diff, self.yaw_diff, self.velocity_diff, self.depth_diff = 0, 0, 0, 0, 0
        
        max_sum_output = 18000.
        self.roll_PID.setMaxOutput(max_sum_output / 4)
        self.pitch_PID.setMaxOutput(max_sum_output / 4)
        self.yaw_PID.setMaxOutput(max_sum_output / 4)
        self.velocity_PID.setMaxOutput(max_sum_output / 4)
        self.depth_PID.setMaxOutput(max_sum_output / 4)

        self.pid_motors_speeds_update = [0, 0, 0, 0, 0]

        self.motors = get_motor_controller(config)
        self.motors.initialize_all()


        self.printer = Printer()
        # self.plotter = Plotter()
    
    def run(self): 
        logging.debug("STARTING PID THREAD")
        self.isActive=True
        while self.active:
            now = time.time_ns()
            self.position_sensor.catch_samples()
            roll = self.position_sensor.get_sample('roll')
            pitch = self.position_sensor.get_sample('pitch')
            yaw = self.position_sensor.get_sample('yaw')
            depth = self.position_sensor.get_sample('depth')
            #print("{} {} {} {}]".format(roll, pitch, yaw,  depth))
            # self.plotter.plot(yaw)
            # print(yaw)
            #print(roll)

            self.roll_diff = self.roll_PID.update(roll)
            self.pitch_diff = self.pitch_PID.update(pitch)
            self.yaw_diff = self.yaw_PID.update(yaw)  # maybe try:  'gyro_raw_x' 'gro_proc_x'
            self.depth_diff = self.depth_PID.update(depth)
            # self.velocity_diff = self.velocity_PID.update(self.IMU.get_sample('vel_x'))

            # prints for testing reasons
            #print(self.roll_PID.last_error)
            # print(self.pitch_diff)
            # print(self.yaw_diff)
            
            with self.lock:
                self.roll_control()
                self.pitch_control()
                self.yaw_control()
                self.pad_control()
                #self.center_x_control()
                #self.depth_control()
                self.update_motors()
            self.printer.set_roll(roll)
            self.printer.set_pitch(pitch)
            self.printer.set_yaw(yaw)
            # self.velocity_control()
            self.printer.print_out()
            
            time.sleep(0.001)
        logging.debug("STOPING PID THREAD")
        self.active = True
        self.isActive = False


    def roll_control(self):
        #exactly like in pitch...
        self.pid_motors_speeds_update[4] += self.roll_diff
        self.pid_motors_speeds_update[2] -= self.roll_diff

    def pitch_control(self):
        #since motors 3 and 4 are inverted in simulaton motor controler '+,+,-' is vertical control...
        self.pid_motors_speeds_update[2] -= self.pitch_diff  # * 2 / 3
        self.pid_motors_speeds_update[4] -= self.pitch_diff  # * 2 / 3
        self.pid_motors_speeds_update[3] -= self.pitch_diff

    def yaw_control(self):
        self.pid_motors_speeds_update[0] += self.yaw_diff
        self.pid_motors_speeds_update[1] -= self.yaw_diff

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
       # data =[]
       # for i in range(5):
            #data.append(random.randint(-1000,1000))
        # print(self.pid_motors_speeds_update)
        self.m =self.pid_motors_speeds_update
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


#GUI methods
    def getIMU(self):
        roll = self.position_sensor.get_sample('roll')
        pitch = self.position_sensor.get_sample('pitch')
        yaw = self.position_sensor.get_sample('yaw')
        depth = self.position_sensor.get_sample('depth')
        return [roll,pitch,yaw,depth]

    def getMotors(self):
        def map(input,in_min,in_max,out_min,out_max):
            return int((input-in_min)*(out_max-out_min)/(in_max-in_min)+out_min)
        ret=[]
        for i in self.m:
            ret.append(map(i, -1000,1000,0,100))
        return ret

    def setPIDs(self, arg):
        if arg[0] == 'roll':
            self.roll_PID.setPIDCoefficients(arg[1],arg[2],arg[3])
        elif arg[0] == 'pitch':
            self.pitch_PID.setPIDCoefficients(arg[1],arg[2],arg[3])
        elif arg[0] == 'yaw':
            self.yaw_PID.setPIDCoefficients(arg[1],arg[2],arg[3])
        elif arg[0] == 'all':
            self.roll_PID.setPIDCoefficients(arg[1],arg[2],arg[3])
            self.pitch_PID.setPIDCoefficients(arg[4],arg[5],arg[5])
            self.yaw_PID.setPIDCoefficients(arg[7],arg[8],arg[9])

    def getPIDs(self,arg):
        if arg=='roll':
            return [arg]+self.roll_PID.getPIDCoefficients()
        elif arg == 'pitch':
            return [arg]+self.pitch_PID.getPIDCoefficients()
        elif arg == 'yaw':
            return [arg]+self.yaw_PID.getPIDCoefficients()
        elif arg == 'all':
            return [arg]+self.roll_PID.getPIDCoefficients()+self.pitch_PID.getPIDCoefficients()+self.yaw_PID.getPIDCoefficients()