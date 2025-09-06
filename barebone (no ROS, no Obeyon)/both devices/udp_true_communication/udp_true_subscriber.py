import asyncio
import socket
import struct
from typing import Callable, Optional, Type
import msgpack
from pydantic import BaseModel
import random

MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 5007

# UNICAST_PUBLISHER_IP = socket.gethostbyname(socket.gethostname())
# UNICAST_PUBLISHER_PORT = 6000+random.randint(0,6000)

class PingFromPublisherMsg(BaseModel):
    topic:str
class PongFromSubscriberMsg(BaseModel):
    topic:str
    unicast_ip:str
    unicast_port:int

class PingFromServiceClientMsg(BaseModel):
    service_name:str
class PongFromServiceServerMsg(BaseModel):
    service_name:str
    unicast_ip:str
    unicast_port:int

class PingFromActionClientMsg(BaseModel):
    action_name:str
class PongFromActionServerMsg(BaseModel):
    action_name:str
    unicast_ip:str
    unicast_port:int
    

class SimpleMessage(BaseModel):
    msg_content:str



class SubscriberProtocol:
    def __init__(self, topic:str, msg_type: Type[BaseModel], on_received_callback:Callable[[BaseModel],None], loop):
        self.loop = loop
        self.transport: Optional[asyncio.DatagramTransport] = None
        self.topic = topic
        self.msg_type = msg_type
        self.on_received_callback=on_received_callback


    def connection_made(self,transport: asyncio.BaseTransport):
        self.transport = transport
        print("Subscriber started")
    
    def datagram_received(self, data, addr):
        packed_msg=data
        dict_msg:dict = msgpack.unpackb(packed_msg)
        print(dict_msg)
        if dict_msg["topic"]==self.topic:
            if dict_msg["type"]=="ping-pubsub-msg":
                dict_msg.pop("type")
                ping_msg = PingFromPublisherMsg(**dict_msg)

                sock = self.transport.get_extra_info('socket')
                # unicast_ip = sock.getsockname()[0]   # subscriber IP
                unicast_ip = socket.gethostbyname(socket.gethostname())
                unicast_port = sock.getsockname()[1] # subscriber port
                pong_msg = PongFromSubscriberMsg(
                    topic=ping_msg.topic,
                    unicast_ip=unicast_ip,
                    unicast_port=unicast_port
                )
                dict_pong_msg = pong_msg.model_dump()
                dict_pong_msg["type"] = "pong-pubsub-msg"

                packed_pong_msg = msgpack.packb(dict_pong_msg)

                self.transport.sendto(packed_pong_msg, (MULTICAST_GROUP, MULTICAST_PORT))
                # self.transport.sendto(packed_pong_msg.encode(), addr)\

                
            elif dict_msg["type"]=="delivery-pubsub-msg":
                dict_msg.pop("type")
                delivery_msg = SimpleMessage(**dict_msg)
                asyncio.create_task(self.on_received_callback(delivery_msg))

    def error_received(self,exc):
        print("Error:", exc)
    
    def connection_lost(self, exc):
        print("Connection closed")

async def listener_callback(msg:SimpleMessage):
    print(f'Publisher => {msg.msg_content}')


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
        lambda: SubscriberProtocol(
            topic="pub&sub",
            msg_type=SimpleMessage,
            on_received_callback=listener_callback,
            loop=loop
        ),
        sock=sock
    )

    try:
        await asyncio.sleep(3600)
    finally:
        transport.close()

if __name__=="__main__":
    asyncio.run(main())