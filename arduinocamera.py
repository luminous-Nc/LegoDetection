import serial
import cv2
import numpy as np


class ArduinoCamera:

    def __init__(self, serial_port, baudrate, bytesize, parity, stopbits):
        self.serial_obj = serial.Serial(serial_port)
        self.serial_obj.baudrate = baudrate
        self.serial_obj.bytesize = bytesize
        self.serial_obj.parity = parity
        self.serial_obj.stopbits = stopbits
        print(f"Serial for arduino ready.")

    def wait_arduino_until_message(self, until_message):
        wait_string = until_message
        res_string = self.serial_obj.readline().decode('UTF-8')
        while res_string != wait_string:
            # print(f'Receive from Serial:{res_string}')
            res_string = self.serial_obj.readline().decode('UTF-8')

    def wait_for_ready(self):
        self.wait_arduino_until_message('Ready for Lego Detection\r\n')
        print('Arduino Board Ready')

    def close(self):
        self.serial_obj.close()

    def set_picture_size(self):
        self.serial_obj.write(bytes([0x05]))
        self.wait_arduino_until_message('ACK CMD switch to OV2640_800x600END\r\n')
        print('Set Picture Size to 800 x 600')

    def get_picture(self):

        self.serial_obj.write(bytes([0x10]))

        # self.wait_arduino_until_message('ACK CMD CAM Capture Done.END\r\n')
        #
        # image_size = self.serial_obj.readline().decode('UTF-8')
        # # print(f"Image Size {image_size}")

        self.wait_arduino_until_message('ACK CMD IMG END\r\n')

        jpg_data = bytearray()

        while True:
            data = self.serial_obj.read()
            jpg_data.append(data[0])
            if len(jpg_data) >= 2 and jpg_data[-2] == 0xff and jpg_data[-1] == 0xD9:
                img_np = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)
                img_np = cv2.flip(img_np, -1)
                return img_np
