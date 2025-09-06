import asyncio
import socket
import struct
import time
from datetime import datetime
import sys

MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 5007
DISCOVERY_INTERVAL = 2  # seconds
BUFFER_SIZE = 1024

# Genereate a unique ID using argument
INSTANCE_ID = sys.argv[1]

# # Generate a unique ID using timestamp
# INSTANCE_ID = datetime.now().strftime("%Y%m%d%H%M%S%f")

# Keep track of discovered peers
discovered_peers = set()

async def send_discovery():
    """
    Periodically send multicast messages to announce presence
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # Enable multicast
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    while True:
        message = INSTANCE_ID.encode('utf-8')
        sock.sendto(message, (MULTICAST_GROUP, MULTICAST_PORT))
        await asyncio.sleep(DISCOVERY_INTERVAL)

async def receive_discovery():
    """
    Listen for multicast messages from other instances
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


    # Allow multiple sockets to use the same PORT (Windows specific)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except AttributeError:
        pass  # Some systems don't support SO_REUSEPORT ex. Linux, Raspberry Pi

    sock.bind(('', MULTICAST_PORT))

    # Join multicast group
    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        try:
            data, addr = await loop.sock_recvfrom(sock, BUFFER_SIZE)
            peer_id = data.decode('utf-8')
            if peer_id != INSTANCE_ID and peer_id not in discovered_peers:
                discovered_peers.add(peer_id)
                print(f"Discovered peer {peer_id} from {addr}")
            else:
                print(f"Received message from already discovered peer {peer_id} from {addr}")
        except Exception as e:
            print("Receive error:", e)
        await asyncio.sleep(0.1)




async def main():
    print(f"My instance ID is {INSTANCE_ID}")
    await asyncio.gather(send_discovery(), receive_discovery())

if __name__ == "__main__":
    asyncio.run(main())
