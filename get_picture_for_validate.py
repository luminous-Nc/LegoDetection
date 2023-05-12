import serial
import time
import numpy as np
import cv2
from ultralytics import YOLO
import json

# check the arduino IDE to find which serial port is connected to main arduino board
SerialObj = serial.Serial('COM7')

# configure the serial port
SerialObj.baudrate = 921600
SerialObj.bytesize = 8
SerialObj.parity = 'N'
SerialObj.stopbits = 1


def init_detect_model():
    model = YOLO('yolov8n.pt')
    return model


def wait_arduino_until_message(until_message):
    wait_string = until_message
    res_string = SerialObj.readline().decode('UTF-8')
    while res_string != wait_string:
        # print(f'Receive from Serial:{res_string}')
        res_string = SerialObj.readline().decode('UTF-8')


def set_picture_size():
    SerialObj.write(bytes([0x05]))
    wait_arduino_until_message('ACK CMD switch to OV2640_800x600END\r\n')
    print('Set Picture Size to 800 x 600')


def detect_picture(model, picture):
    results = model.predict(source=picture, conf=0.12)
    boxes = results[0].boxes
    names = results[0].names
    classes = boxes.cls
    objects = [names[int(x)] for x in classes]
    num_persons = objects.count('person')
    annotated_frame = results[0].plot(masks=True, line_width=None)
    return num_persons, annotated_frame


def get_picture():
    SerialObj.write(bytes([0x10]))

    wait_arduino_until_message('ACK CMD CAM Capture Done.END\r\n')

    image_size = SerialObj.readline().decode('UTF-8')
    # print(f"Image Size {image_size}")

    wait_arduino_until_message('ACK CMD IMG END\r\n')

    jpg_data = bytearray()

    while True:
        data = SerialObj.read()
        jpg_data.append(data[0])
        if len(jpg_data) >= 2 and jpg_data[-2] == 0xff and jpg_data[-1] == 0xD9:
            img_np = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            img_np = cv2.flip(img_np, -1)
            return img_np

def write_picture_and_number(picture, file_index,people_number):
    picture_name = f"test_pic_{file_index}-{people_number}.jpg"
    cv2.imwrite(f"new_validate/{picture_name}", picture)
    print(f'save {picture_name} with people number {people_number}')
    return file_index, people_number

if __name__ == "__main__":
    print ("Begin to collect image")
    wait_arduino_until_message('Ready for Lego Detection\r\n')
    print('Arduino Board Ready')
    set_picture_size()

    file_index = 151

    while True:
        picture = get_picture()
        cv2.imshow('Get image', picture)
        key = cv2.waitKey(1)

        if key == ord('1'):
            people_number = 1
            picture_name, people_number = write_picture_and_number(picture, file_index, people_number)
            file_index+=1
        if key == ord('2'):
            people_number = 2
            picture_name, people_number = write_picture_and_number(picture, file_index, people_number)
            file_index += 1
        if key == ord('3'):
            people_number = 3
            picture_name, people_number = write_picture_and_number(picture, file_index, people_number)
            file_index += 1
        if key == ord('4'):
            people_number = 4
            picture_name, people_number = write_picture_and_number(picture, file_index, people_number)
            file_index += 1
        if key == ord('0'):
            people_number = 0
            picture_name, people_number = write_picture_and_number(picture, file_index, people_number)
            file_index += 1
        if key == ord('Q'):
            break
    cv2.destroyAllWindows()
    SerialObj.close()
