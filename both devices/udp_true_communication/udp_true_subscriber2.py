import asyncio
import socket
import struct
from typing import Callable, Optional, Type
import msgpack
from pydantic import BaseModel
import random

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


class DiscoveryPongerForSubscriber_UDPMulticastProtocol:
    #domain id -> MULTICAST_GROUP, MULTICAST_PORT
    pass

class DiscoveryPongerForSubscriber:
    pass

class MessageReceiverForSubscriber_WebSocketProtocol:
    pass

class MessageReceiverForSubscriber:
    pass


class Subscriber:
    def __init__(self, )
    pass