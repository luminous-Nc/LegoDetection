from ultralytics import YOLO
import cv2


class LegoDetector:
    def __init__(self, model, conf, lego_class_name):
        self.predict_model = YOLO(model)
        self.conf = conf
        self.lego_class_name = lego_class_name
        print(f"Detector is ready")

    def detect_lego_people(self, picture):
        results = self.predict_model.predict(source=picture, conf=self.conf)
        boxes = results[0].boxes
        names = results[0].names
        classes = boxes.cls
        objects = [names[int(x)] for x in classes]
        num_persons = objects.count(self.lego_class_name)
        annotated_frame = results[0].plot(masks=True, line_width=None)
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottom_left_corner_of_text = (10, 30)
        font_scale = 1
        font_color = (255, 255, 255)
        line_type = 2
        annotate_string = f"{num_persons} lego people"
        cv2.putText(annotated_frame, annotate_string, bottom_left_corner_of_text, font, font_scale, font_color,
                    line_type)
        return num_persons, annotated_frame
