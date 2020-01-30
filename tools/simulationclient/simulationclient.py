import socket
from struct import *
import logging
import time
import json


class SimulationClient:
    """Klasa Tworzy clienta do odbierania ramek zdjec z symulacji"""
    def __init__(self, port=44210, ip='localhost'):
        """Inicjalizacja socekta """
        self.port = port
        self.ip = ip
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug("Socket connect port:{}".format(port))
        self.socket.connect((self.ip, self.port))
        logging.debug("Socket now Connect with port:{}".format(port))
        self.motors_data = {"FL":0.1,"FR":-1.0,"ML":0.1,"MR":0.0,"B":0.008}
        self.data =  b""

    def __del__(self):
        self.socket.close()

    def set_motors(self, motors_data):
        if len(motors_data) == 5:
            self.motors_data["FL"] = motors_data[0]
            self.motors_data["FR"] = motors_data[1]
            self.motors_data["ML"] = motors_data[2]
            self.motors_data["MR"] = motors_data[3]
            self.motors_data["B"] = motors_data[4]
            serialized = json.dumps(self.motors_data).encode('ascii')
            lenght = pack('<I', len(serialized))
            self.socket.send(b"\xA0"+lenght)
            self.socket.sendall(serialized)
            print("send")

    def get_pos(self):
        self.data = b""
        self.socket.send(b"\xC2\x00\x00\x00\x00")
        #print("Send")
        confirm = self.socket.recv(1)
        #print(confirm)
        if not(confirm == b"\xC2"):
            return None
            logging.debug("Message error")
        lenght = self.socket.recv(4)
        lenght = unpack('<I', lenght)[0]
        #print(lenght)
        while not(len(self.data) >= lenght):
            self.data += self.socket.recv(4096)

        ack = self.data[lenght:]
        return json.loads(self.data[:lenght])