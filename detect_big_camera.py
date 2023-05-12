# Get picture from NexiGo-Webcam N60 and detect the numbers of Lego Minifigures

import cv2
import time
from legodetector import LegoDetector
from global_setting import *


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Could not open camera")
        exit()

    detector = LegoDetector(model=detect_model_name, conf=detect_conf, lego_class_name=detect_class_name)

    while cap.isOpened():
        success, frame = cap.read()

        if success:
            picture = frame
            lego_people_num, result_image = detector.detect_lego_people(picture)
            cv2.imshow("Detect Lego with USB Camera", result_image)

            # Control the detection interval if needed
            if enable_detect_interval:
                time.sleep(detect_interval)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break
    cv2.destroyAllWindows()
    cap.release()
