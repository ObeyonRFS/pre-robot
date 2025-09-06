import asyncio
import socket

MULTICAST_GROUP = "224.1.1.1"
MULTICAST_PORT = 5007
UNICAST_PORT = 6000

class PublisherProtocol:
    def __init__(self, loop):
        self.loop = loop
        self.transport = None
        self.subscribers = set()

    def connection_made(self, transport):
        self.transport = transport
        print("Publisher started")

        # Periodically announce on multicast
        self.loop.create_task(self.announce())

    async def announce(self):
        while True:
            msg = b"DISCOVER:publisher"
            self.transport.sendto(msg, (MULTICAST_GROUP, MULTICAST_PORT))
            print(f"Sent multicast discovery: {msg.decode()}")
            await asyncio.sleep(3)

    def datagram_received(self, data, addr):
        message = data.decode()
        print(f"Received from {addr}: {message}")

        if message.startswith("SUBSCRIBER:"):
            self.subscribers.add(addr)
            print(f"Registered subscriber: {addr}")

            # Send direct unicast
            self.transport.sendto(b"PUBLISHER_MESSAGE:Hello subscriber!", addr)

    def error_received(self, exc):
        print("Error:", exc)

    def connection_lost(self, exc):
        print("Connection closed")


async def main():
    loop = asyncio.get_running_loop()

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", UNICAST_PORT))

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: PublisherProtocol(loop),
        sock=sock
    )

    try:
        # await asyncio.sleep(3600)
        print("This message indicate that the code still executable for another task")
        await asyncio.sleep(10)
        
    finally:
        transport.close()

if __name__ == "__main__":
    asyncio.run(main())
