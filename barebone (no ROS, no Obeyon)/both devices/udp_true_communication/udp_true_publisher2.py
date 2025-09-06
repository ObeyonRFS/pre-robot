import asyncio
import socket
from typing import Optional, Type
import msgpack
from pydantic import BaseModel
import random

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

class DiscoveryPingForPublisher_Protocol:

class MessageRe

class Publisher:
    pass


MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 5007