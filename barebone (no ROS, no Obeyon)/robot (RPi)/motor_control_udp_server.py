import asyncio
import json
import serial
import esp32_finder
import time

# --- Serial Setup ---
ports = esp32_finder.find_possible_ESP32_ports()
if len(ports) != 1:
    raise SystemExit("ESP32 not found or too many devices")

ser = serial.Serial(port=ports[0], baudrate=115200, timeout=1)
time.sleep(2)

clients = set()  # track client addresses


def send_to_esp32(message: dict):
    json_str = json.dumps(message)
    ser.write((json_str + "\n").encode("utf-8"))
    print(f"➡️ Sent to ESP32: {json_str}")


class UDPServerProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("🌐 UDP server ready")

    def datagram_received(self, data, addr):
        clients.add(addr)  # remember sender
        try:
            message = json.loads(data.decode())
            send_to_esp32(message)
        except json.JSONDecodeError:
            print(f"⚠️ Invalid JSON from {addr}: {data!r}")

    def send_to_clients(self, msg: str):
        for addr in clients:
            self.transport.sendto(msg.encode(), addr)


async def serial_reader(protocol: UDPServerProtocol):
    loop = asyncio.get_event_loop()
    while True:
        line = ser.readline().decode().strip()
        if line:
            print(f"⬅️ From ESP32: {line}")
            protocol.send_to_clients(line)
        await asyncio.sleep(0.01)


async def main():
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPServerProtocol(),
        local_addr=("0.0.0.0", 8765)
    )
    try:
        await serial_reader(protocol)
    finally:
        transport.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")
