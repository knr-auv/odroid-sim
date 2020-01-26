import threading
import time
import pickle
from variable import motors_speed, motors_speed_pad, run_flag, IP_ADDRESS_2, PAD_PORT, SAVE_FLAG, MOVES_FILE


class ReadSteeringThread(threading.Thread):
    """Thread class that play primitive steering by commands from file """
    def __init__(self, pid_thread, config):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.pid_thread = pid_thread
        self.file = None

        # strojenie regulatorow #hardcoded
        pid_thread.roll_PID.setPIDCoefficients(config.get_pid("roll", "P"), config.get_pid("roll", "I"),
                                               config.get_pid("roll", "D")) # zahardkodowane narazie # nastawy  z testow
        pid_thread.pitch_PID.setPIDCoefficients(config.get_pid("pitch", "P"), config.get_pid("pitch", "I"),
                                                config.get_pid("pitch", "D"))
        pid_thread.yaw_PID.setPIDCoefficients(config.get_pid("yaw", "P"), config.get_pid("pitch", "I"),
                                              config.get_pid("pitch", "P")) # zera, bo horyzontalnymi silnikami sterujemy tylko plikiem

    def run(self):
        global motors_speed, run_flag, motors_speed_pad
        self.file = open(MOVES_FILE, "rb")
        while True:
            try:
                data_frame = pickle.load(self.file)
                #print(data_frame)
            except(EOFError, pickle.UnpicklingError):
                with self.lock:
                    self.pid_thread.pid_motors_speeds_update[0] = 0
                    self.pid_thread.pid_motors_speeds_update[1] = 0
                    self.pid_thread.pid_motors_speeds_update[2] = 0
                    self.pid_thread.pid_motors_speeds_update[3] = 0
                    self.pid_thread.pid_motors_speeds_update[4] = 0
                    #print("KONIEC")
                    break

            with self.lock:
               if len(data_frame) == 6:
                    motor_0_duty = data_frame[0]
                    motor_1_duty = data_frame[1]
                    roll_offset = data_frame[2]
                    pitch_offset = data_frame[3]
                    #depth_offset = data_frame[4]
                    vertical_duty = data_frame[4] # bez glebokosciomierza

                    time.sleep(data_frame[5]) # usypiamy na dany czas

                    motors_speed_pad[0] = (-0.5)*motor_0_duty
                    motors_speed_pad[1] = (-0.5)*motor_1_duty
                    motors_speed_pad[2] = 0.3*vertical_duty
                    motors_speed_pad[3] = 0.3*vertical_duty
                    motors_speed_pad[4] = 0.3*vertical_duty
                    self.pid_thread.roll_PID.setSetPoint(roll_offset)
                    self.pid_thread.pitch_PID.setSetPoint(pitch_offset)
                    print(data_frame)
                    #self.pid_thread.depth_PID.setSetPoint(depth_offset)  # can't use without depth funcionalities