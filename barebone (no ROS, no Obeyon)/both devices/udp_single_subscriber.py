import asyncio
import socket
import struct

MULTICAST_GROUP = "224.1.1.1"
MULTICAST_PORT = 5007
# UNICAST_PORT = 6000

class SubscriberProtocol:
    def __init__(self, loop):
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("Subscriber started")

    def datagram_received(self, data, addr):
        message = data.decode()
        print(f"Received from {addr}: {message}")

        if message.startswith("DISCOVER:publisher"):
            # Respond directly to publisher
            print("Respond to publisher")
            # self.transport.sendto(b"SUBSCRIBER:hello", (addr[0], UNICAST_PORT))
            self.transport.sendto(b"SUBSCRIBER:hello", (addr[0], addr[1]))
        elif message.startswith("PUBLISHER_MESSAGE:"):
            pass

    def error_received(self, exc):
        print("Error:", exc)

    def connection_lost(self, exc):
        print("Connection closed")

async def main():
    loop = asyncio.get_running_loop()

    # Create UDP socket for multicast listening
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", MULTICAST_PORT))

    # Join multicast group
    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: SubscriberProtocol(loop),
        sock=sock
    )

    try:
        await asyncio.sleep(3600)
    finally:
        transport.close()

if __name__ == "__main__":
    asyncio.run(main())
