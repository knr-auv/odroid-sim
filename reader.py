import os
import time


def read_log():
    with open('output.log', 'r') as input:
        os.system('clear')
        print(input.read())
        time.sleep(0.2)


while True:
    read_log()
