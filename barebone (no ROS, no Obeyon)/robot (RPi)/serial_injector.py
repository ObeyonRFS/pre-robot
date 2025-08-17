import serial
import esp32_finder
import sys
import json


if __name__=="__main__":
    ports=esp32_finder.find_possible_ESP32_ports()
    if len(ports)>1:
        print("There are too many usb serial device")
        sys.exit(1)
    elif len(ports)==0:
        print("There is no usb serial device")
        sys.exit(1)

    ser = serial.Serial(port=ports[0], baudrate=115200, timeout=1)
    time.sleep(2)

    def set_motor_power(left, right):
        # prepare JSON message
        message = {
            "command": "set_motor_power",
            "parameters": {
                "L": left,
                "R": right
            }
        }
        # convert to JSON string
        json_str = json.dumps(message)
        # send with newline at the end (ESP32 waits for \n)
        ser.write((json_str + "\n").encode("utf-8"))
        print(f"Sent: {json_str}")

    # example usage
    set_motor_power(255, 0)
    time.sleep(1)
    set_motor_power(100, 150)

    # optionally read feedback from ESP32
    while True:
        line = ser.readline().decode().strip()
        if line:
            print(f"ESP32: {line}")


    
# import serial
# import json
# import time

# # open serial port (adjust COM port or /dev/ttyUSBx)
# ser = serial.Serial(port="COM3", baudrate=115200, timeout=1)

# time.sleep(2)  # give ESP32 time to reset

# def set_motor_power(left, right):
#     # prepare JSON message
#     message = {
#         "command": "set_motor_power",
#         "parameters": {
#             "L": left,
#             "R": right
#         }
#     }
#     # convert to JSON string
#     json_str = json.dumps(message)
#     # send with newline at the end (ESP32 waits for \n)
#     ser.write((json_str + "\n").encode("utf-8"))
#     print(f"Sent: {json_str}")

# # example usage
# set_motor_power(255, 0)
# time.sleep(1)
# set_motor_power(100, 150)

# # optionally read feedback from ESP32
# while True:
#     line = ser.readline().decode().strip()
#     if line:
#         print(f"ESP32: {line}")
