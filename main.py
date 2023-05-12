import serial
import time
import numpy as np
import cv2
from ultralytics import YOLO

# check the arduino IDE to find which serial port is connected to main arduino board
SerialObj = serial.Serial('COM7')

# configure the serial port
SerialObj.baudrate = 921600
SerialObj.bytesize = 8
SerialObj.parity = 'N'
SerialObj.stopbits = 1

detect_class_name = 'Lego-People'
detect_conf = 0.25


def init_detect_model():
    model = YOLO('lego_detection_model.pt')
    return model


def wait_arduino_until_message(until_message):
    wait_string = until_message
    res_string = SerialObj.readline().decode('UTF-8')
    while res_string != wait_string:
        print(f'Receive from Serial:{res_string}')
        res_string = SerialObj.readline().decode('UTF-8')


def set_picture_size():
    SerialObj.write(bytes([0x05]))
    wait_arduino_until_message('ACK CMD switch to OV2640_800x600END\r\n')
    print('Set Picture Size to 800 x 600')


def detect_picture(model, picture):
    results = model.predict(source=picture, conf=detect_conf)
    boxes = results[0].boxes
    names = results[0].names
    classes = boxes.cls
    objects = [names[int(x)] for x in classes]
    num_persons = objects.count(detect_class_name)
    annotated_frame = results[0].plot(masks=True, line_width=None)
    return num_persons, annotated_frame


def get_picture():
    SerialObj.write(bytes([0x10]))

    wait_arduino_until_message('ACK CMD CAM Capture Done.END\r\n')

    image_size = SerialObj.readline().decode('UTF-8')
    print(f"Image Size {image_size}")

    wait_arduino_until_message('ACK CMD IMG END\r\n')

    jpg_data = bytearray()

    while True:
        data = SerialObj.read()
        jpg_data.append(data[0])
        if len(jpg_data) >= 2 and jpg_data[-2] == 0xff and jpg_data[-1] == 0xD9:
            img_np = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            img_np = cv2.flip(img_np, -1)
            return img_np


if __name__ == "__main__":

    wait_arduino_until_message('Ready for Lego Detection\r\n')
    print('Arduino Board Ready')
    set_picture_size()

    detect_model = init_detect_model()
    while True:
        picture = get_picture()

        num, result = detect_picture(detect_model, picture)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bottom_left_corner_of_text = (10, 30)
        font_scale = 1
        font_color = (255, 255, 255)
        line_type = 2
        annotate_string = f"{num} people"
        cv2.putText(result, annotate_string, bottom_left_corner_of_text, font, font_scale, font_color,
                    line_type)

        cv2.imshow("Small Camera Detect", result)

        time.sleep(1)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
    SerialObj.close()