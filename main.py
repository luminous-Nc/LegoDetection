import time
import numpy as np
import cv2
from ultralytics import YOLO
import detect_lego
from arduinocamera import ArduinoCamera
from legodetector import LegoDetector
detect_model_name = "lego_detection_model.pt"
detect_class_name = 'Lego-People'
detect_conf = 0.25

Port = 'COM7'
Baudrate = 921600
Bytesize = 8
Parity = 'N'
Stopbits = 1


if __name__ == "__main__":
    arduino_camera = ArduinoCamera(serial_port=Port,baudrate=Baudrate,bytesize=Bytesize,parity=Parity,stopbits=Stopbits)
    arduino_camera.wait_for_ready()
    arduino_camera.set_picture_size()

    detector = LegoDetector(model=detect_model_name,conf=detect_conf,lego_class_name=detect_class_name)
    while True:
        picture = arduino_camera.get_picture()

        lego_people_num, result = detector.detect_lego_people(picture)

        cv2.imshow("Small Camera Detect", result)


        # time.sleep(1)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
    arduino_camera.close()