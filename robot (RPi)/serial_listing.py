import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"Device: {port.device}")
    print(f"  Name: {port.name}")
    print(f"  Description: {port.description}")
    print(f"  HWID: {port.hwid}")
    print(f"  VID: {port.vid}, PID: {port.pid}")
    print(f"  Serial number: {port.serial_number}")
    print("-----")