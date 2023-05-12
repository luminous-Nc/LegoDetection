# check the arduino IDE to find which serial port is connected to main arduino board
detect_model_name = "lego_detection_model.pt"
detect_class_name = 'Lego-People'
detect_conf = 0.75

# configure the serial port
Port = 'COM7'
Baudrate = 921600
Bytesize = 8
Parity = 'N'
Stopbits = 1