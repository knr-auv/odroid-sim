from control.autonomy.target import Target
import time
import threading

#from .PID import *
from tools.connection.connectionOdroid import *
from variable import IP_ADDRESS_2, JETSON_PORT, motors_speed_pad

# IP_ADDRESS_1 = '10.41.0.42'  # address jetson
# IP_ADDRESS_2 = '10.41.0.42'  # address odroid
# PORT = 8181
SEARCH_MAX_ANGLE_ABS = 60.  # maksymalny kąt rozglądania się



class Autonomy(threading.Thread):
    """Class that implements all autonomy -> methods that will controll AUV depending on
    what cameras see, what they saw and when and also decides in what order perform realising tasks,
    when there are many possibilities.
    Will be run in thread or maybe will inherit from Thread class"""
    def __init__(self, pid_thread, config):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.pid_thread = pid_thread
        self.position_sensor = self.pid_thread.get_position_sensor()

        #self.pid_follow_obj = PID()

        # tworzenie obiektu wątku połączenia z jetsonem
        self.conn = Connection(IP_ADDRESS_2, JETSON_PORT)
        #self.conn = conn_thread  # gdyby był podawany wątek w konstruktorze
        self.conn.start()

        self.raw_data_frame = []
        self.target_position = []
        self.target_last_seen_position = []
        self.cam_num = 0
        self.max_searching_time = 10  # sec

        # aktualny cel do którego zmierzamy
        self.target = Target()
        pid_thread.roll_PID.setPIDCoefficients(4, 2, 2) # zahardkodowane narazie # nastawy  z testow
        pid_thread.pitch_PID.setPIDCoefficients(10, 2, 1)
        pid_thread.yaw_PID.setPIDCoefficients(2, 0, 0)
        pid_thread.depth_PID.setPIDCoefficients(30, 0, 0)
        pid_thread.depth_PID.setSetPoint(1)

        global motors_speed_pad

    def run(self):
        catch_detections_thread = threading.Thread(target=self.catch_detections)
        catch_detections_thread.start()

        time.sleep(10)
        self.look_for_detections()

    def catch_detections(self):
        # łapanie ramek danych i wpisywanie ich w pola, których bedziemy uzywac do sterowania
        while True:
            with self.lock:
                self.raw_data_frame = self.conn.getDataFrame()
                self.target.update_target_position(self.raw_data_frame)
                self.target_position, self.cam_num = self.target.get_target_position()
                self.target_last_seen_position, _k = self.target.get_target_prev_position()
                # if self.target.get_flag():
                #     print("MAM")

    def look_for_detections(self):
        #self.prev_pid_values = self.pid_thread.center_x_PID.getPIDCoefficients()
        #self.pid_thread.center_x_PID
        self.stop()
        #self.pid_thread.yaw_PID.setSetPoint(0.)
        time.sleep(1)
        # motors_speed_pad[0] = 200
        # motors_speed_pad[1] = 200
        # time.sleep(1)
        # motors_speed_pad[0] = 0
        # motors_speed_pad[1] = 0
        time.sleep(2)

        print("ZACZYNA SZUKAC")
        while not(self.target.get_flag()): #and (time.time() - self.target.last_time) < self.max_searching_time:
            yaw = self.position_sensor.get_sample('yaw')
            # max angle w stopniach -> zakres 'rozglądania się' łodzi
            if (yaw > - SEARCH_MAX_ANGLE_ABS and yaw < 0) or (yaw > SEARCH_MAX_ANGLE_ABS):
                self.turning_left(-10.)  # 10 deg/sec
                time.sleep(0.5)
            elif (yaw > 0 and yaw < SEARCH_MAX_ANGLE_ABS) or (yaw < - SEARCH_MAX_ANGLE_ABS):
                self.turning_right(-10.)  # 10 deg/sec
                time.sleep(0.5)

        #jezeli nie znalazł i szukał wiecej niz 10 sec to płyń do przodu i znowu szukaj (głupie troche)
        # if not (self.target.get_flag()):
        #     motors_speed_pad[0] = 200
        #     motors_speed_pad[1] = 200
        #     time.sleep(3)
        #     self.look_for_detections()
        # else:
        self.stop()
        self.follow_object(self.target_position[1:3],(4, 1, 0), 200) # TODO: pid val
        # tutaj jakas decyzja ktory obiekt sledzic?
        # [PRZECZYTAJ] Moze od razu szukajmy danego biektu jesli nie zdnajdziemy w danym czasie zmieniamy cel?
        # [PRZECZYTAJ] Wymaga dopracowania moze jazda do przodu po jakims czasie i tam się rozejrzenie
        # no i wywolanie sledzenia


    def turning_left(self, vel):
        self.pid_thread.yaw_PID.setSetPoint(self.pid_thread.yaw_PID.getSetPoint() - vel)

    def turning_right(self, vel):
        self.pid_thread.yaw_PID.setSetPoint(self.pid_thread.yaw_PID.getSetPoint() + vel)

    def follow_object(self, center_offset, pid_values, velocity):
        print("FOLLOW DAMN TRAIN")
        # Nic pewnego czy zadziała narazie
        # TODO: odkomentowac rzeczy zwiazane z depth_PID kiedy on bedzie robiony w wątku z PIDami
        self.prev_yaw_pid_values = self.pid_thread.yaw_PID.getPIDCoefficients()
        # self.prev_depth_pid_values = self.pid_thread.depth_PID.getPIDCoefficients()  # odkomentowac jak bedzie depth_PID zrobiony :)

        # turn off yaw_PID, żeby mozna bylo sterowac tylko za pomocą offsetu z kamery
        self.pid_thread.yaw_PID.setPIDCoefficients(0., 0., 0.)
        # self.pid_thread.depth_PID.setPIDCoefficients(0., 0., 0.)  # odkomentowac jak bedzie depth_PID zrobiony :)
        self.pid_thread.center_x_PID.setPIDCoefficients(pid_values[0], pid_values[1], pid_values[2])
        while self.target.get_flag():
            obstacles = self.target.get_obstacles_to_avoid()
            if len(obstacles) == 0:
                self.pid_thread.center_x_PID.center_x_diff = self.pid_thread.center_x_PID.update(center_offset[0])  # x
                #self.pid_thread.center_y_PID.center_y_diff = self.pid_thread.center_y_PID.update(center_offset[1])  # y # odkomentowac jak bedzie depth_PID zrobiony :)
                self.forward(velocity)
            else:
                pass # tu logika do wymijania obiektow

        # jeśli nie widzi obiektu przez dłuzszy czas to znowu wywołuje 'rozgladanie sie'
        # ora przywroc poprzednie nastawy PID
        # [PRZECZYTAJ] Warunek wyjścia potrzebny
        self.pid_thread.yaw_PID.setPIDCoefficients(self.prev_yaw_pid_values[0], self.prev_yaw_pid_values[1],
                                                   self.prev_yaw_pid_values[2])
        # self.pid_thread.depth_PID.setPIDCoefficients(self.prev_yaw_pid_values[0], self.prev_yaw_pid_values[1], # odkomentowac jak bedzie depth_PID zrobiony :)
        #                                            self.prev_yaw_pid_values[2])
        # self.look_for_detections()

    def hit_object(self):
        # TODO: warunek
        self.follow_object(self.target_position[1:3], 100)
        # TODO: warunek na oststnie widziane wypełnienie obrazu obiektem i odleglosci do obiektu
        if self.target.get_time_of_view() > 2:
            self.forward(500)
            time.sleep(2)
            self.stop()


    def forward(self, velocity):
        motors_speed_pad[0] = velocity
        motors_speed_pad[1] = velocity

    def backward(self, velocity):
        self.pid_thread.pid_motors_speeds_update[0] = -velocity
        self.pid_thread.pid_motors_speeds_update[1] = -velocity

    def stop(self):
        self.pid_thread.pid_motors_speeds_update[0] = 0
        self.pid_thread.pid_motors_speeds_update[1] = 0

    """Nawrot i beczka wymagaja wprowadzenia licznika liczby obrotow, zeby mozna bylo wyregulowac po obrocie o 360.
    Dla nawrotu nalezy w ogole przemapowac katy do domyslnych wartosci. Licznik concept: zmiana kata na imu 
    z 360 do 0 - l+=1, z -360 do 0 l-=1. W ten sposob mozna byloby zdeterminowac, że obrot zostal zrobiony czy nie.
    Na razie przed nawrotem ustawi sie do kata 0 osi Z, nastepnie obroci sie o 160 stopni, zeby nie przejsc za 180"""
    def barrel_roll(self):
        self.pid_thread.yaw_PID.setSetPoint(self.pid_thread.roll_PID.getSetPoint + 360)
        sleep(5)
        self.pid_thread.yaw_PID.setSetPoint(0)

    def nawrot(self):
        self.pid_thread.yaw_PID.setSetPoint(0)
        self.forward(800)
        sleep(3)
        self.stop()
        self.turning_right(160)
        sleep(3)
        self.forward(800)
        sleep(3)
        self.stop()


