import serial.tools.list_ports
from typing import List
def find_possible_ESP32_ports() -> List[str]:
    ports = serial.tools.list_ports.comports()
    r=[]
    for port in ports:
        if port.description=="USB Serial":
            r.append(port.device)
    return r



if __name__=="__main__":
    print(find_possible_ESP32_ports())