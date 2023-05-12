import numpy as np
import cv2
from ultralytics import YOLO
import json
import glob
import matplotlib.pyplot as plt


def count_people_number():
    people_counts = {}

    image_files = glob.glob("new_validate/*.jpg")

    for image_file in image_files:
        filename = image_file.split("/")[-1]
        people_number = int(filename.split("-")[-1].split(".")[0])
        if people_number in people_counts:
            people_counts[people_number] += 1
        else:
            people_counts[people_number] = 1
    print(people_counts)
    plt.bar(people_counts.keys(), people_counts.values())
    plt.xlabel('People Number')
    plt.ylabel('Count')
    plt.title('Counts of People Number in New Validate Dataset')
    plt.show()


def init_detect_model():
    model = YOLO('lego.pt')
    return model


def detect_picture(model, picture):
    results = model.predict(source=picture, conf=0.12)
    boxes = results[0].boxes
    names = results[0].names
    classes = boxes.cls
    objects = [names[int(x)] for x in classes]

    num_persons = objects.count('person') + objects.count('parking meter') + objects.count('fire hydrant')
    annotated_frame = results[0].plot(masks=True, line_width=None)
    return num_persons, annotated_frame


def read_real_picture(image_file):
    filename = image_file.split("/")[-1]
    people_number = int(filename.split("-")[-1].split(".")[0])
    return people_number


if __name__ == "__main__":
    count_people_number()
    detect_model = init_detect_model()
    image_files = glob.glob("new_validate/*.jpg")
    real_people_numbers = []
    detected_people_numbers = []

    real_have_people = []
    detected_have_people = []

    for image_file in image_files:
        image = cv2.imread(image_file)
        real_num_persons = read_real_picture(image_file)

        real_people_numbers.append(real_num_persons)
        if real_num_persons != 0:
            real_have_people.append(True)
        else:
            real_have_people.append(False)

        detect_num_persons, annotated_frame = detect_picture(detect_model, image)
        detected_people_numbers.append(detect_num_persons)
        if detect_num_persons != 0:
            detected_have_people.append(True)
        else:
            detected_have_people.append(False)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bottom_left_corner_of_text = (10, 30)
        font_scale = 1
        font_color = (255, 255, 255)
        line_type = 2
        annotate_string = f"{detect_num_persons} people"
        cv2.putText(annotated_frame, annotate_string, bottom_left_corner_of_text, font, font_scale, font_color,
                    line_type)
        write_name = image_file.split("\\")[-1]
        print(write_name)
        cv2.imwrite(f"new_validate_result\\{write_name}", annotated_frame)

        print(f"Detect {image_file}, should have {real_num_persons} people, detect {detect_num_persons} people")

    number_accuracy = sum([a == d for a, d in zip(real_people_numbers, detected_people_numbers)]) / len(
        real_people_numbers) * 100
    have_accuracy = sum([b == e for b, e in zip(real_have_people, detected_have_people)]) / len(real_have_people) * 100

    print(f"Detection Number of People Accuracy : {number_accuracy}%")
    print(f"Detection People Exist Accuracy : {have_accuracy}%")

    x = ["Number Correct", "Number Incorrect","Exist Correct","Exist Incorrect"]
    y = [number_accuracy, 100 - number_accuracy, have_accuracy, 100 - have_accuracy]
    plt.bar(x, y)
    plt.title("Detection Number & Exist Accuracy")
    plt.xlabel("Accuracy")
    plt.ylabel("Percentage")
    plt.show()
