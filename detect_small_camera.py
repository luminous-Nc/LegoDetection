# Get picture from ArduCam small SPI camera modules and detect the numbers of Lego Minifigures

import cv2
from arduinocamera import ArduinoCamera
from legodetector import LegoDetector
from global_setting import *

if __name__ == "__main__":
    arduino_camera = ArduinoCamera(serial_port=Port,baudrate=Baudrate,bytesize=Bytesize,parity=Parity,stopbits=Stopbits)
    arduino_camera.wait_for_ready()
    arduino_camera.set_picture_size()

    detector = LegoDetector(model=detect_model_name,conf=detect_conf,lego_class_name=detect_class_name)
    while True:
        picture = arduino_camera.get_picture()

        lego_people_num, result_image = detector.detect_lego_people(picture)

        cv2.imshow("Small Camera Detect", result_image)

        # Control the detection interval if needed
        # time.sleep(1)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
    arduino_camera.close()