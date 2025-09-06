import asyncio
import websockets
import cv2

async def send_images():
    uri = "ws://TUFMATO.local:8412"
    async with websockets.connect(uri) as websocket:
        cap = cv2.VideoCapture(0)  # webcam
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Encode frame as JPEG
            _, buffer = cv2.imencode(".jpg", frame)

            # Send bytes over WebSocket
            await websocket.send(buffer.tobytes())

            await asyncio.sleep(0.03)  # ~30fps

asyncio.run(send_images())
