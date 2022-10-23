import serial
import serial.tools.list_ports
import numpy as np


class SerialController:

    def __init__(self):
        self.frame_buff = bytearray()
        self.is_connected = False

    def update(self):
        waiting_count = self.serial.in_waiting

        if waiting_count > 0:
            frame = self.serial.read(waiting_count)
            return self.__parse_input(frame)
        else:
            return None

    def reset(self):
        self.frame_buff = bytearray()

    def connect(self):
        com_port = self.find_esp32_port()

        if com_port != None:
            print("Trying to connect to serial ({})...".format(com_port))
            self.serial = serial.Serial(com_port, baudrate=115200, timeout=1)
            self.is_connected = True
            print("Successfully connected to serial {}".format(self.serial.name))
        else:
            raise serial.SerialException("Can't find ESP32 COM port")

    def disconnect(self):
        self.serial.close()
        self.is_connected = False

    def find_esp32_port(self):
        ports = serial.tools.list_ports.comports()

        for p in ports:
            if "USB-SERIAL CH340" in p.description:
                print("Found ESP32 on port {}".format(p.name))
                return p.name

        pretty_ports = ''.join("--> {}\n".format(p.description) for p in ports)
        print("Can't find ESP32 in given ports:\n{}".format(pretty_ports))
        return None

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


if __name__ == "__main__":
    serial_controller = SerialController()
    serial_controller.find_esp32_port()
