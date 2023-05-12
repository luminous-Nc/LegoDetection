import cv2
import glob
import matplotlib.pyplot as plt
from legodetector import LegoDetector
from global_setting import *

validate_folder_name = 'new_validate'
# validate_folder_name = 'validate'


def count_label_number():
    people_counts = {}

    image_files = glob.glob(f"{validate_folder_name}/*.jpg")

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
    plt.title(f'Counts of People Number in {validate_folder_name} Dataset')
    for i, v in enumerate(people_counts.values()):
        plt.text(i, v, str(v), ha='center', va='bottom', fontweight='bold')
    plt.show()


def read_real_picture(image_file):
    filename = image_file.split("/")[-1]
    people_number = int(filename.split("-")[-1].split(".")[0])
    return people_number


if __name__ == "__main__":
    count_label_number()

    detector = LegoDetector(model=detect_model_name, conf=detect_conf, lego_class_name=detect_class_name)
    image_files = glob.glob(f"{validate_folder_name}/*.jpg")

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

        detect_num_persons, annotated_frame = detector.detect_lego_people(image)
        detected_people_numbers.append(detect_num_persons)
        if detect_num_persons != 0:
            detected_have_people.append(True)
        else:
            detected_have_people.append(False)

        write_name = image_file.split("\\")[-1]
        cv2.imwrite(f"{validate_folder_name}_result\\{write_name}", annotated_frame)

        print(f"Detect {image_file}, should have {real_num_persons} people, detect {detect_num_persons} people")

    number_accuracy = sum([a == d for a, d in zip(real_people_numbers, detected_people_numbers)]) / len(
        real_people_numbers) * 100
    have_accuracy = sum([b == e for b, e in zip(real_have_people, detected_have_people)]) / len(real_have_people) * 100

    print(f"Detection Number of People Accuracy : {number_accuracy}%")
    print(f"Detection People Exist Accuracy : {have_accuracy}%")

    x = ["Number Correct", "Number Incorrect", "Exist Correct", "Exist Incorrect"]
    y = [number_accuracy, 100 - number_accuracy, have_accuracy, 100 - have_accuracy]
    plt.bar(x, y)
    plt.title("Detection Number & Exist Accuracy")
    plt.xlabel("Accuracy")
    plt.ylabel("Percentage")
    for i, v in enumerate(y):
        plt.text(i, v, str(v) + '%', ha='center', va='bottom', fontweight='bold')
    plt.show()
