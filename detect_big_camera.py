import cv2
from ultralytics import YOLO

if __name__ == '__main__':

    cap = cv2.VideoCapture(0)

    model = YOLO('yolov8n.pt')

    if not cap.isOpened():
        print("Could not open camera")
        exit()

    detect_flag = False

    while cap.isOpened():

        success, frame = cap.read()

        if success:
            results = model.predict(source=frame, conf=0.12)
            boxes = results[0].boxes
            names = results[0].names
            classes = boxes.cls
            objects = [names[int(x)] for x in classes]
            num_persons = objects.count('person')
            if num_persons == 0:
                print('no person')
                pass
            elif num_persons == 1:
                print('1 people')
                pass
            elif num_persons == 2:
                print('2 people')
                pass
            elif num_persons == 3:
                print('3 people')
                pass
            else:
                print('more than 3 people')
                pass

            annotated_frame = results[0].plot(masks=True, line_width=None)

            cv2.imshow("Detect Big Camera", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
