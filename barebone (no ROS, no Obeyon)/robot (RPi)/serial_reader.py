import serial
import time

# Replace 'COM3' with your ESP32 port
# On Linux/Mac it could be '/dev/ttyUSB0' or '/dev/ttyACM0'
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for ESP32 to reset
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit()

print("Reading motor RPM... Press Ctrl+C to stop.")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(line)
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
