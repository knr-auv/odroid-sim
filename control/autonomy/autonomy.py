from control.autonomy.target import Target
import time
import threading
import random


from tools.connection.connectionOdroid import *
from variable import *


SEARCH_MAX_ANGLE_ABS = 60.  # maksymalny kąt rozglądania się



class Autonomy(threading.Thread):
    """Class that implements all autonomy -> methods that will controll AUV depending on
    what cameras see, what they saw and when and also decides in what order perform realising tasks,
    when there are many possibilities.
    It inherit from Thread class"""
    def __init__(self, pid_thread, config):
        print('autonomy 1')
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.pid_thread = pid_thread
        self.position_sensor = self.pid_thread.get_position_sensor()

        # tworzenie obiektu watku polaczenia z jetsonem
        self.conn = Connection(IP_ADDRESS_2, JETSON_PORT)
        # self.conn = conn_thread  # gdyby byl podawany watek w konstruktorze

        self.raw_data_frame = []
        self.target_position = []
        self.target_last_seen_position = []
        self.cam_num = 0
        self.max_searching_time = 10  # sec

        # aktualny cel do ktorego zmierzamy
        self.target = Target()

        # ONLY FOR SIMULATION SETTING RANDOM P:
        rand = - random.randrange(7,15)
        config.get_client().set_orien([-10, 0.3, -5.], [0., 0., 0.])
        print(' pozycja wylosowana X: ', rand)

        # ustawienie PID-kow
        pid_thread.roll_PID.setPIDCoefficients(4, 2, 2)
        pid_thread.pitch_PID.setPIDCoefficients(10, 2, 1)
        pid_thread.yaw_PID.setPIDCoefficients(4, 1, 0)
        pid_thread.depth_PID.setPIDCoefficients(200, 0.05, 5) # ernest's 200;0;0
        pid_thread.depth_PID.setWindup(1)
        pid_thread.center_x_PID.setPIDCoefficients(0.18, 0.14, 0.03) # TODO: pid val
        pid_thread.center_y_PID.setPIDCoefficients(0.18, 0, 0) # TODO: pid val
        pid_thread.center_x_PID.turn_off() # Na poczatku uzywamy tylko yaw_PID
        pid_thread.center_y_PID.turn_off()
        pid_thread.depth_PID.setSetPoint(1.1)
        pid_thread.center_x_PID.setSetPoint(0)
        pid_thread.center_x_PID.setSetPoint(0)

        # pid_thread.yaw_PID.turn_off()
        global motors_speed_pad


    def run(self):
        # uruchamianie watkow komunikacyjinych
        self.conn.start()
        catch_detections_thread = threading.Thread(target=self.catch_detections)
        catch_detections_thread.start()

        print('Diving... sleep 30sec')
        time.sleep(30)

        #rozpoczecie dzialania autonomii
        while True:
            # SZUKANIE POZYCJI
            print("START")
            while True:
                print("ROZGLADANIE")
                self.stop()
                flag = self.look_for_target()
                if flag:
                    break
                print("ZMINAN POZYCJI")
                self.stop()
                flag = self.change_position()
                if flag:
                    break

            print("ZNALEZIONO")
            self.stop()
            lost_flag = self.follow_object(200)

            print(lost_flag)

            # if True:
            # if not lost_flag:
            #     break
            #     self.target.change_target()
            # else:
            #     break #tu akcja zwiazana z targetem po osiagnieciu go

        print("KONIEC")

    def catch_detections(self):
        # lapanie ramek danych i wpisywanie ich w pola, ktorych bedziemy uzywac do sterowania
        prev_time = time.time()
        while True:
            with self.lock:
                self.raw_data_frame = self.conn.getDataFrame()
                self.target.update_target_position(self.raw_data_frame)
                self.target_position, self.cam_num = self.target.get_target_position()
                self.target_last_seen_position, _k = self.target.get_target_prev_position()
                if time.time() - prev_time > 0.1:
                    self.pid_thread.center_x_PID.update(self.target_position[0])
                    self.pid_thread.center_y_PID.update(self.target_position[1])
                    prev_time = time.time()
            # print('Diff: x,y : ', self.pid_thread.center_x_PID.get_diff(), self.pid_thread.center_y_PID.get_diff())
            # print('Target pos: ', self.target_position[0], self.pid_thread.center_x_PID.get_diff())
                # if self.target.get_flag():
                #     print("MAM")

    def change_position(self):
        self.forward(200)
        time.sleep(3.)
        with self.lock:
            flag = self.target.get_flag()
        # print(flag)
        if flag:
            return True
        self.stop()

        return False

    def look_for_target(self):

        # jezeli widzi juz cel
        with self.lock:
            # print (self.target.get_flag())
            if self.target.get_flag():
                return True

        self.stop()
        # flag = self.wait_and_check(1.)
        # if flag:
        #     return True

        print("OBROTY")
        for i in range(5):
            self.turning_left(10.)  # 10 deg/sec
            time.sleep(0.5)
            with self.lock:
                flag = self.target.get_flag()
            # print(flag)
            if flag:
                return True

        for i in range(10):
            self.turning_right(10.)  # 10 deg/sec
            time.sleep(0.5)
            with self.lock:
                flag = self.target.get_flag()
            # print(flag)
            if flag:
                return True

        for i in range(5):
            self.turning_left(10.)  # 10 deg/sec
            time.sleep(0.5)
            with self.lock:
                flag = self.target.get_flag()
            # print(flag)
            if flag:
                return True

        #time.sleep(5)

        # while not(self.target.get_flag()): #and (time.time() - self.target.last_time) < self.max_searching_time:
        #     yaw = self.position_sensor.get_sample('yaw')
        #     # max angle w stopniach -> zakres 'rozgladania sie' lodzi
        #     if (yaw > - SEARCH_MAX_ANGLE_ABS and yaw < 0) or (yaw > SEARCH_MAX_ANGLE_ABS):
        #         self.turning_left(-10.)  # 10 deg/sec
        #         flag =  self.wait_and_check(0.5)
        #         if flag:
        #             return True
        #     elif (yaw > 0 and yaw < SEARCH_MAX_ANGLE_ABS) or (yaw < - SEARCH_MAX_ANGLE_ABS):
        #         self.turning_right(-10.)  # 10 deg/sec
        #         flag = self.wait_and_check(0.5)
        #         if flag:
        #             return True

        #jezeli nie znalazl i szukal wiecej niz 10 sec to plyn do przodu i znowu szukaj (glupie troche)
        with self.lock:
            if not (self.target.get_flag()):
                return False

        return True

    def turning_left(self, vel):
        self.pid_thread.yaw_PID.setSetPoint(self.pid_thread.yaw_PID.getSetPoint() - vel)

    def turning_right(self, vel):
        self.pid_thread.yaw_PID.setSetPoint(self.pid_thread.yaw_PID.getSetPoint() + vel)

    def bypassing_obstacles(self):
        pass #tu sposob omijania przeszkod

    def follow_object(self, velocity):

        # zeby mozna bylo sterowac tylko za pomoca offsetu z kamery
        with self.lock:
            self.pid_thread.yaw_PID.turn_off()
            self.pid_thread.center_x_PID.turn_on()
            self.pid_thread.depth_PID.turn_off()
            self.pid_thread.center_y_PID.turn_on()

        self.forward(velocity)

        start = time.time()

        # self.forward(200)
        # time.sleep(10)
        # self.stop()
        # print("STOP")
        # time.sleep(10)
        # with self.lock:
        #     self.pid_thread.yaw_PID.turn_on()
        #     self.pid_thread.center_x_PID.turn_off()
        # return False
        stop = True

        while stop:
            # obstacles = self.target.get_obstacles_to_avoid()
            # if len(obstacles) > 0:
            #     self.bypassing_obstacles()
            if self.target.get_time_of_view() > 2. and self.target.get_fill_level() > 70.:
                print("PIZDA DO PRZODU")
                with self.lock:
                    self.pid_thread.yaw_PID.setSetPoint(self.pid_thread.position_sensor.get_sample('yaw'))
                    self.pid_thread.yaw_PID.turn_on()
                    self.pid_thread.center_x_PID.turn_off()
                    self.pid_thread.depth_PID.setSetPoint(self.pid_thread.position_sensor.get_sample('depth'))
                    self.pid_thread.depth_PID.turn_on()
                    self.pid_thread.center_y_PID.turn_off()
                self.forward(300)
                time.sleep(5)
                self.stop()
                print("STOP")
                time.sleep(10)

                return False
            with self.lock:
                stop = self.target.get_flag()

        # wrucenie do normalnych nastaw
        with self.lock:
            self.pid_thread.yaw_PID.setSetPoint(self.pid_thread.position_sensor.get_sample('yaw'))
            self.pid_thread.yaw_PID.turn_on()
            self.pid_thread.center_x_PID.turn_off()
            self.pid_thread.depth_PID.setSetPoint(self.pid_thread.position_sensor.get_sample('depth'))
            self.pid_thread.depth_PID.turn_on()
            self.pid_thread.center_y_PID.turn_off()
        return True

    def hit_object(self):
        # TODO: warunek
        self.follow_object(self.target_position[1:3])
        # TODO: warunek na oststnie widziane wypełnienie obrazu obiektem i odleglosci do obiektu
        if self.target.get_time_of_view() > 2:
            self.forward(500)
            time.sleep(2)
            self.stop()

    def forward(self, velocity):
        motors_speed_pad[0] = velocity
        motors_speed_pad[1] = velocity


    def backward(self, velocity):
        motors_speed_pad[0] = -velocity
        motors_speed_pad[1] = -velocity

    def stop(self):
        motors_speed_pad[0] = 0
        motors_speed_pad[1] = 0

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

