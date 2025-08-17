import serial
import esp32_finder
import sys
import json
import time

if __name__=="__main__":
    ports = esp32_finder.find_possible_ESP32_ports()
    if len(ports) > 1:
        print("There are too many usb serial devices")
        sys.exit(1)
    elif len(ports) == 0:
        print("There is no usb serial device")
        sys.exit(1)

    ser = serial.Serial(port=ports[0], baudrate=115200, timeout=1)
    time.sleep(2)  # wait for ESP32 to reboot

    def set_motor_power(left, right):
        message = {
            "command": "set_motor_power",
            "parameters": {"L": left, "R": right}
        }
        json_str = json.dumps(message)
        ser.write((json_str + "\n").encode("utf-8"))
        print(f"Sent: {json_str}")

    print("✅ Ready. Type motor power values like: 200 150")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("Enter L R: ").strip()
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Exiting...")
                break

            parts = user_input.split()
            if len(parts) != 2:
                print("⚠️ Please enter two numbers (L R)")
                continue

            try:
                L = int(parts[0])
                R = int(parts[1])
            except ValueError:
                print("⚠️ Invalid numbers")
                continue

            set_motor_power(L, R)

            # also check ESP32 response
            line = ser.readline().decode().strip()
            if line:
                print(f"ESP32: {line}")

        except KeyboardInterrupt:
            print("\nStopped by user")
            break
