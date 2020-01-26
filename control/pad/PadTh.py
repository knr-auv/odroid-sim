import threading
import time
import pickle
from variable import motors_speed, motors_speed_pad, run_flag, IP_ADDRESS_2, PAD_PORT, SAVE_FLAG, MOVES_FILE
from tools.connection import Connection


class PadSteeringThread(threading.Thread):
    """Thread class that is terminal's UI for setting PIDs, primitive steering by commands """
    def __init__(self, pid_thread, config):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.pid_thread = pid_thread
        self.last_time = time.time()

        # stworzenie wątków do odczytu danych z pada
        self.connection = Connection(IP_ADDRESS_2, PAD_PORT)
        self.read_values_thread = threading.Thread(target=self.connection)


        # strojenie regulatorow #hardcoded
        pid_thread.roll_PID.setPIDCoefficients(4, 2, 2) # zahardkodowane narazie # nastawy  z testow
        pid_thread.pitch_PID.setPIDCoefficients(10, 2, 1)
        pid_thread.yaw_PID.setPIDCoefficients(0, 0, 0) # zera, bo horyzontalnymi silnikami sterujemy tylko padem

    def run(self):
        global motors_speed, motors_speed_pad, run_flag
        self.connection.start()
        while True:
            data_frame = self.connection.getDataFrame()
            with self.lock:
                if len(data_frame) == 5:
                    motor_0_duty = data_frame[0]
                    motor_1_duty = data_frame[1]
                    roll_offset = data_frame[2]
                    pitch_offset = data_frame[3]
                    #depth_offset = data_frame[4]
                    vertical_duty = data_frame[4] # bez glebokosciomierza

                    motors_speed_pad[0] = (-0.5)*motor_0_duty
                    motors_speed_pad[1] = (-0.5)*motor_1_duty
                    motors_speed_pad[2] = 0.3*vertical_duty
                    motors_speed_pad[3] = 0.3*vertical_duty
                    motors_speed_pad[4] = 0.3*vertical_duty
                    self.pid_thread.roll_PID.setSetPoint(roll_offset)
                    self.pid_thread.pitch_PID.setSetPoint(pitch_offset)
                    if SAVE_FLAG:
                        self.save(data_frame)
                    # print(data_frame)
                    #self.pid_thread.depth_PID.setSetPoint(depth_offset)  # can't use without depth funcionalities

    def save(self, data_frame):
        with open(MOVES_FILE, 'ab') as file:
            data_frame.append(time.time()-self.last_time)
            self.last_time = time.time()
            file.write(pickle.dumps(data_frame))