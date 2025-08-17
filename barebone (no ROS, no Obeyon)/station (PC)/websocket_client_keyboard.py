import asyncio
import websockets
import json
import keyboard  # pip install keyboard

# --- Motor mapping ---
# Adjust these values based on your motor configuration
KEY_TO_MOTOR = {
    'w': {"L": 255, "R": 255},   # forward
    's': {"L": -255, "R": -255}, # backward
    'a': {"L": -150, "R": 150},  # turn left
    'd': {"L": 150, "R": -150},  # turn right
}

async def run_client():
    uri = "ws://urpi.local:8765"  # replace with server IP
    async with websockets.connect(uri) as websocket:
        print("✅ Connected to server. Press W/A/S/D to control, Q to quit.")

        while True:
            try:
                # Check keys in real-time
                for key in KEY_TO_MOTOR:
                    if keyboard.is_pressed(key):
                        message = {
                            "command": "set_motor_power",
                            "parameters": KEY_TO_MOTOR[key]
                        }
                        await websocket.send(json.dumps(message))
                        print(f"➡️ Sent: {message}")
                        await asyncio.sleep(0.1)  # repeat rate
                        
                if keyboard.is_pressed('q'):
                    print("Exiting...")
                    return

                await asyncio.sleep(0.01)

            except websockets.ConnectionClosed:
                print("❌ Disconnected from server")
                break

if __name__ == "__main__":
    asyncio.run(run_client())
