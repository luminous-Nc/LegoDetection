import serial


if __name__ == "__main__":
    print('BEGIN to RUN')

    # Open the serial port
    ser = serial.Serial('COM8', 9600)  # Replace 'COM1' with the appropriate port and 9600 with the correct baud rate

    while True:
        # Read the data from the serial port
        message = ser.readline()

        # Decode the message assuming it's encoded as UTF-8
        decoded_message = message

        # Print the message
        print(decoded_message)

    # Close the serial port (unreachable in this code as it's in an infinite loop)
    ser.close()