import serial
import numpy as np


class SerialController:

    def __init__(self):
        self.frame_buff = bytearray()
        self.serial = serial.Serial('COM6', baudrate=115200, timeout=1)
        print("Successfully connected to serial")

    def update(self):
        waiting_count = self.serial.in_waiting

        if waiting_count > 0:
            frame = self.serial.read(waiting_count)
            return self.__parse_input(frame)
        else:
            return None

    def close(self):
        self.serial.close()

    def __parse_input(self, frame):
        new_frame = False

        frames = []

        for c in np.frombuffer(frame, dtype='S1'):
            if c == b'[':
                new_frame = True
                self.frame_buff = bytearray()
            elif c == b']' and new_frame == True:
                values = self.frame_buff.decode().split(',')
                frames.append([int(values[0]), int(values[1])])
                new_frame = False
            else:
                self.frame_buff += c

        if len(frames) > 0:
            return frames[-1]
        else:
            return None
