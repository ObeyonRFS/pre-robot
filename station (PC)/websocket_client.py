import asyncio
import websockets
import json

async def run_client():
    uri = "ws://urpi.local:8765"
    async with websockets.connect(uri) as websocket:
        print("✅ Connected to server")

        # Example: send motor power command
        message = {
            "command": "set_motor_power",
            "parameters": {"L": 200, "R": 100}
        }
        await websocket.send(json.dumps(message))
        print(f"➡️ Sent: {message}")

        # Listen for messages
        try:
            while True:
                response = await websocket.recv()
                print(f"⬅️ From server: {response}")
        except websockets.ConnectionClosed:
            print("❌ Disconnected from server")

if __name__ == "__main__":
    asyncio.run(run_client())
