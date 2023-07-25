from ultralytics import YOLO

# Load a model

if __name__ == "__main__":
    model = YOLO('../yolov8n.pt')  # load a pretrained model (recommended for training)
    # Train the model
    model.train(data='lego_people.yaml', epochs=100, imgsz=640)