import asyncio
import websockets
import json
import keyboard as kb  # pip install keyboard

# --- Motor mapping ---
power_min = 100
power_max = 255

KEY_TO_MOTOR = {
    'w': {"L": 1, "R": 1},    # forward
    's': {"L": -1, "R": -1},  # backward
    'a': {"L": -0.5, "R": 0.5},  # turn left
    'd': {"L": 0.5, "R": -0.5},  # turn right
}

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

async def send_motor_commands(websocket):
    while True:
        if kb.is_pressed("q"):
            print("Exiting")
            break

        percentL = 0.0
        percentR = 0.0
        amplitude = 2/3

        if kb.is_pressed("up"):
            amplitude += 1/3
        if kb.is_pressed("down"):
            amplitude -= 1/3

        for key in KEY_TO_MOTOR:
            if kb.is_pressed(key):
                percentL += KEY_TO_MOTOR[key]["L"] * amplitude
                percentR += KEY_TO_MOTOR[key]["R"] * amplitude

        # Always send, even if percentL and percentR are zero
        powerL:int=0
        powerR:int=0
        if percentL!=0.0 or percentR!=0.0:
            powerL = sign(percentL) * int(power_min + (power_max - power_min) * abs(percentL))
            powerR = sign(percentR) * int(power_min + (power_max - power_min) * abs(percentR))

        message = {
            "command": "set_motor_power",
            "parameters": {"L": powerL, "R": powerR}
        }

        await websocket.send(json.dumps(message))
        print(f"➡️ Sent: {message}")

        await asyncio.sleep(0.5)

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
