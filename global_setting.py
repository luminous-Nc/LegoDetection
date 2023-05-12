# Global Settings for detection model and connection to Arduino board.

# Use trained lego detection model to detect
detect_model_name = "lego_detection_model.pt"
detect_class_name = 'Lego-People'
# Detection confidence threshold
detect_conf = 0.75

# configure the serial port
# Check Device Manager to define the Port number for Arduino Board
Port = 'COM7'
Baudrate = 921600
Bytesize = 8
Parity = 'N'
Stopbits = 1

# configure the detect interval
enable_detect_interval = True
detect_interval = 10
