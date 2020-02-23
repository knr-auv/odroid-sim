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
        self.motors_data = {"FL":0.0,"FR":0.0,"ML":0.0,"MR":0.0,"B":0.0}
        self.orien_data = {"rot": {"x": 0.0, "y": 0.0, "z": 0.0}, "pos": {"x": 0.0, "y": 0.0, "z": 0.0}}
        self.data =  b""
        self.ack = b""

    def __del__(self):
        self.socket.close()

    def set_motors(self):
        self.ack = b""
        serialized = json.dumps(self.motors_data).encode('ascii')
        lenght = pack('<I', len(serialized))
        self.socket.send(b"\xA0"+lenght)
        self.socket.sendall(serialized)
        # print(serialized)
        # COMMENT
        # confirm = self.socket.recv(1)
        # lenght = self.socket.recv(4)
        # lenght = unpack('<I', lenght)[0]
        # self.ack += self.socket.recv(lenght)

    def set_orien(self, pos, rot):
        if len(pos) == 3 and len(rot) == 3:
            self.ack = b""
            self.orien_data["pos"]["x"] = pos[0]
            self.orien_data["pos"]["y"] = pos[1]
            self.orien_data["pos"]["z"] = pos[2]
            self.orien_data["rot"]["x"] = rot[0]
            self.orien_data["rot"]["y"] = rot[1]
            self.orien_data["rot"]["z"] = rot[2]
            serialized = json.dumps(self.orien_data).encode('ascii')
            lenght = pack('<I', len(serialized))
            self.socket.send(b"\xC3"+lenght)
            self.socket.sendall(serialized)

    def get_pos(self):
        self.data = b""
        self.socket.send(b"\xC2\x00\x00\x00\x00")
        #print("Send")
        confirm = self.socket.recv(1)
        #print(confirm)
        if not(confirm == b"\xC2"):
            logging.debug("Message error")
            return None
        lenght = self.socket.recv(4)
        lenght = unpack('<I', lenght)[0]
        #print(lenght)
        while not(len(self.data) >= lenght):
            self.data += self.socket.recv(4096)

        # ack = self.data[lenght:]
        return json.loads(self.data[:lenght])

    def get_sens(self):
        self.data = b""
        self.socket.send(b"\xB0\x00\x00\x00\x00")
        #print("Send")
        confirm = self.socket.recv(1)
        #print(confirm)
        if not(confirm == b"\xB0"):
            logging.debug("Message error")
            # print(confirm)
            return None
        lenght = self.socket.recv(4)
        lenght = unpack('<I', lenght)[0]
        #print(lenght)
        while not(len(self.data) >= lenght):
            self.data += self.socket.recv(4096)

        # ack = self.data[lenght:]
        # print(ack)
        return json.loads(self.data[:lenght])