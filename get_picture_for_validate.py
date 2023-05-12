import serial
import numpy as np
import cv2
from arduinocamera import ArduinoCamera

Port = 'COM7'
Baudrate = 921600
Bytesize = 8
Parity = 'N'
Stopbits = 1

file_begin_index = 151


def write_picture_and_number(picture, file_index, people_number):
    picture_name = f"test_pic_{file_index}-{people_number}.jpg"
    cv2.imwrite(f"new_validate/{picture_name}", picture)
    print(f'save {picture_name} with people number {people_number}')
    return file_index, people_number


if __name__ == "__main__":
    print("Begin to collect image")
    arduino_camera = ArduinoCamera(serial_port=Port, baudrate=Baudrate, bytesize=Bytesize, parity=Parity,
                                   stopbits=Stopbits)
    arduino_camera.wait_for_ready()
    arduino_camera.set_picture_size()

    while True:
        picture = arduino_camera.get_picture()
        cv2.imshow('Get image', picture)
        key = cv2.waitKey(1)

        if key == ord('1'):
            people_number = 1
            picture_name, people_number = write_picture_and_number(picture, file_begin_index, people_number)
            file_begin_index += 1
        if key == ord('2'):
            people_number = 2
            picture_name, people_number = write_picture_and_number(picture, file_begin_index, people_number)
            file_begin_index += 1
        if key == ord('3'):
            people_number = 3
            picture_name, people_number = write_picture_and_number(picture, file_begin_index, people_number)
            file_begin_index += 1
        if key == ord('4'):
            people_number = 4
            picture_name, people_number = write_picture_and_number(picture, file_begin_index, people_number)
            file_begin_index += 1
        if key == ord('0'):
            people_number = 0
            picture_name, people_number = write_picture_and_number(picture, file_begin_index, people_number)
            file_begin_index += 1
        if key == ord('Q'):
            break
    cv2.destroyAllWindows()
    arduino_camera.close()
