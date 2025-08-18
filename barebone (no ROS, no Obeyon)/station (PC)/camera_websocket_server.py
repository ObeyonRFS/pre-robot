import asyncio
import websockets
import cv2
import numpy as np

async def handler(websocket):
    async for message in websocket:
        # Decode image from bytes
        np_arr = np.frombuffer(message, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow("Received", frame)
            cv2.waitKey(1)

async def main():
    async with websockets.serve(handler, "TUFMATO.local", 8412):
        print("Server running at ws://TUFMATO.local:8412")
        await asyncio.Future()  # run forever

asyncio.run(main())
