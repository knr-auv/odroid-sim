import time


class Target:
    """Class that represent current target object that will be our destiny"""
    def __init__(self):
        # Na razie tylko koncepcja klasy Celu z listą priorytetow ktora wybiera cel do ktorego mamy jechac
        self.priority_list = [b'GATE', b'STRING']  # Lista priorytetow
        self.priority_list_pointer = 0  # Ktora lista priorytetów jest wybrana
        self.last_time = time.time()  # Czas kiedy cel byl osatnio widziany
        self.max_time = 1 # Maksymalny czas bez wykrycia celu
        self.obstacle = []  # Lista przeszkod widzianych przez kamere
        self.obstacle_to_avoid = []

        # POZYCJA
        self.position = [0, 0]
        self.distance = []
        self.last_seen_position = []
        self.last_seen_distance = []

        # WYPELNIENIE EKRANU
        self.fill_level = 0


        # FLAGI
        self.obstacle_flag = False
        self.target_flag = False
        self.prev_target_flag = False # Teraz nie widzi targetu ale poprzednio widzial
        self.lost_target_flag = False  # Czy zgubil target - jezeli False to znaczy, ze jeszcze nie zgubil
        self.first_view_time = None
        self.cam = None
        self.finish_flag = False  # Czy koniec targetoww



    def update_target_position(self, objects_detected_frame):
        self.prev_target_flag = self.target_flag
        # self.lost_target_flag = False
        tmp_flag = False

        self.obstacle.clear()
        if len(objects_detected_frame) >= 2:
            for obj in objects_detected_frame[0]:
                if obj[4][0] == self.priority_list[self.priority_list_pointer]:
                    self.position = obj[1:3]
                    self.fill_level = obj[3]
                    tmp_flag = True
                    self.cam = 0
                    if self.first_view_time is None:
                        self.first_view_time = time.time()
                else:
                    self.obstacle.append(obj)
                    self.obstacle_flag = True
            for obj in objects_detected_frame[1]:
                if obj[4][0] == self.priority_list[self.priority_list_pointer]:
                    self.position = obj[1:3]
                    self.fill_level = obj[3]
                    tmp_flag = True
                    self.cam = 1
                    if self.first_view_time is None:
                        self.first_view_time = time.time()
                else:
                    self.obstacle.append(obj)
                    self.obstacle_flag = True

        if tmp_flag:
            # jezeli widzi target i ostatnio widzial, to uaktualnij poprzednio widziana pozycje
            if self.prev_target_flag:
                self.last_seen_position = self.position
            self.last_time = time.time()
            self.target_flag = True
        else:
            # jezeli nie widzi targetu, ale ostatnio widzial to ustaw flage
            if self.prev_target_flag:
                self.lost_target_flag = True
            # jezeli przekroczyl max czas bycia zgubionym to zmien target -> nastepne zadanie
            if (time.time() - self.last_time) > self.max_time:
                self.target_flag = False
        self.check_obstacles()

    """Return
        True - koniec celi
        False - mamy kolejny cel
        """
    def change_target(self):
        if self.priority_list_pointer < 1:
            self.priority_list_pointer += 1  # Zwiększenie priorytetu o 1
            self.first_view_time = None
            self.position = [420, 150]
            self.distance.clear()
            self.cam = None
            self.target_flag = False
            self.prev_target_flag = False  # na wypadek jak przełączy i w pierwszej ramce już znajdzie target
            self.finish_flag = False
        else:
            self.finish_flag = True

    """Sprawdzanie czy obiekt jest na drodze"""
    def check_obstacles(self):
        pass # tutaj warunek, że obiekt jest na naszej drodze i trzeba go ominąć, dodanie so self.obstacles_to_avoid

    """Return Obstacles to avoid data"""
    def get_obstacles_to_avoid(self):
        return self.obstacle_to_avoid

    """Return target position and camera"""
    def get_target_position(self):
        return self.position, self.cam

    """Retrun target distance and camera"""
    def get_target_distance(self):
        return self.distance, self.cam

    """Return target previous position and camera"""
    def get_target_prev_position(self):
        return self.position, self.cam

    """Retrun target previous distance and camera"""
    def get_target_prev_distance(self):
        return self.distance, self.cam

    """Return time of view target"""
    def get_time_of_view(self):
        if self.first_view_time is None:
            return 0
        else:
            return time.time() - self.first_view_time

    """Return find flag"""
    def get_flag(self):
        return self.target_flag

    """Return Target fill_level"""
    def get_fill_level(self):
        return self.fill_level

