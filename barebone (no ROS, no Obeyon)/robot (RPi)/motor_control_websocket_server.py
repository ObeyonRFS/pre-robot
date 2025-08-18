import asyncio
import json
import serial
import esp32_finder
import time
import websockets

# --- Serial Setup ---
ports = esp32_finder.find_possible_ESP32_ports()
if len(ports) != 1:
    raise SystemExit("ESP32 not found or too many devices")

ser = serial.Serial(port=ports[0], baudrate=115200, timeout=1)
time.sleep(2)

# --- Send JSON to ESP32 ---
def send_to_esp32(message: dict):
    json_str = json.dumps(message)
    ser.write((json_str + "\n").encode("utf-8"))
    print(f"➡️ Sent to ESP32: {json_str}")

# --- Read loop from ESP32 ---
async def serial_reader(websocket_set):
    while True:
        line = ser.readline().decode().strip()
        if line:
            print(f"⬅️ From ESP32: {line}")
            # forward to all websocket clients
            if websocket_set:
                await asyncio.gather(*[ws.send(line) for ws in websocket_set])
        await asyncio.sleep(0.01)

# --- WebSocket handler ---
async def handler(websocket):
    connected.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                send_to_esp32(data)
            except json.JSONDecodeError:
                await websocket.send("⚠️ Invalid JSON")
    finally:
        connected.remove(websocket)

# --- Main ---
connected = set()

async def main():
    # Start websocket server
    server = await websockets.serve(handler, "0.0.0.0", 8765)
    print("🌐 WebSocket server running on ws://0.0.0.0:8765")

    # Run both tasks: websocket + serial reader
    await asyncio.gather(
        server.wait_closed(),
        serial_reader(connected)
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")
