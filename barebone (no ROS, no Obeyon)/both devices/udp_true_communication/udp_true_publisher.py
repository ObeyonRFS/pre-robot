import asyncio
import socket
from typing import Optional, Type
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


class PublisherProtocol:
    def __init__(self, topic:str, msg_type:Type[BaseModel], loop):
        self.loop = loop
        self.transport: Optional[asyncio.DatagramTransport] = None
        self.subscribers_unicast_location = set()
        self.topic = topic
        self.msg_type = msg_type

    def connection_made(self, transport: asyncio.BaseTransport):
        self.transport = transport
        print("Publisher started")

        self.loop.create_task(self.announce())

    async def announce(self):
        while True:
            ping_msg = PingFromPublisherMsg(
                topic=self.topic,
                pong_state=False
            )
            dict_msg=ping_msg.model_dump()
            dict_msg["type"]="ping-pubsub-msg"
            packed_msg = msgpack.packb(dict_msg)
            self.transport.sendto(packed_msg, (MULTICAST_GROUP, MULTICAST_PORT))
            # print(f"Perform PING")
            await asyncio.sleep(1)

    def datagram_received(self,data,addr):
        packed_msg = data
        dict_msg:dict = msgpack.unpackb(packed_msg)
        if dict_msg["topic"]==self.topic:
            if dict_msg["type"]=="pong-pubsub-msg":
                dict_msg.pop("type")
                pong_msg = PongFromSubscriberMsg(**dict_msg)
                self.subscribers_unicast_location.add(
                    (pong_msg.unicast_ip,pong_msg.unicast_port)
                )

    def error_received(self, exc):
        print("Error:", exc)
    
    def connection_lost(self, exc):
        print("Connection closed")

    async def publish(self,delivery_msg:BaseModel):
        for (unicast_sub_ip,unicast_sub_port) in self.subscribers_unicast_location:
            dict_msg=delivery_msg.model_dump()
            dict_msg["type"]="delivery-pubsub-msg"
            packed_msg = msgpack.packb(dict_msg)
            self.transport.sendto(packed_msg, (unicast_sub_ip, unicast_sub_port))

async def main():
    loop = asyncio.get_running_loop()
    transport,protocol = await loop.create_datagram_endpoint(
        lambda: PublisherProtocol(topic="pub&sub", msg_type=SimpleMessage, loop=loop),
        local_addr=(socket.gethostbyname(socket.gethostname()),0)
    )

    try:
        print("This message indicate that the code still executable for another task")
        
        while True:
            print("Sending message to subscriber")
            delivery_msg = SimpleMessage(msg_content="Hello subscribers")
            await protocol.publish(delivery_msg)

            await asyncio.sleep(2)
    finally:
        transport.close()

if __name__=="__main__":
    asyncio.run(main())









