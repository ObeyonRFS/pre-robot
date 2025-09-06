import asyncio
import websockets
import json
import keyboard as kb

KEY_TO_MOTOR = {
    'w': {"L": 20, "R": 20},    # forward
    's': {"L": -20, "R": -20},  # backward
    'a': {"L": -15, "R": 15},  # turn left
    'd': {"L": 15, "R": -15},  # turn right
    'space': {"L": 0, "R": 0},
}


async def send_motor_commands(websocket):
    prev_key = None
    while True:
        if kb.is_pressed("q"):
            print("Exiting")
            break

        speedL=0
        speedR=0
        new_key = None
        for key in KEY_TO_MOTOR:
            if kb.is_pressed(key):
                speedL = KEY_TO_MOTOR[key]["L"]
                speedR = KEY_TO_MOTOR[key]["R"]
                new_key = key
                break

        if prev_key != new_key:
            message = {
                "command": "set_motor_speed",
                "parameters":{
                    "L":speedL,
                    "R":speedR,
                }
            }

            await websocket.send(json.dumps(message))
            print(f"➡️ Sent: {message}")

        prev_key=new_key

        await asyncio.sleep(0.001)


async def receive_messages(websocket):
    try:
        async for message in websocket:
            print(f"⬅️ From server: {message}")
    except websockets.ConnectionClosed:
        print("❌ Disconnected from server")

async def run_client():
    uri = "ws://urpi.local:8765"  # replace with server IP
    async with websockets.connect(uri) as websocket:
        print("✅ Connected to server. Press W/A/S/D to control, Q to quit.")

        # Run send and receive concurrently
        await asyncio.gather(
            send_motor_commands(websocket),
            receive_messages(websocket)
        )

if __name__ == "__main__":
    asyncio.run(run_client())