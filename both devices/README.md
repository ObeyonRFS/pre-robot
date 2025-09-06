# Notices
`udp_single_publisher.py` and `udp_single_subscriber.py`

you can't run multiple instance of it. Their codes is very simple to read, But it can explain about UDP multicast normally

- The UDP Multicast sender don't know the destination on where to sent back when received message, 
    - and sent back through UDP multicast protocol also can make a wasted traffic
        - wasted traffic can be critical for sendind heavy message like "image"
- UDP multicast is more about publisher and subscriber rather server and client like other.
- 



# Take back for Obeyon
- Node shouldn't act as Antenna
    - let communicators do direct communication each other
        - publisher to subscriber
        - service client and service server
        - action server and action client
    - let publisher communicate with subscriber directly
- UDP and Websocket
    - multicast mode for discovery
        - MULTICAST_GROUP, and MULTCAST_PORT will be configurable by user
            - This is like domain id in ROS, but more physical config
                - This is ok really
    - ~~unicast mode for data delivery~~
        - ~~msgpack might be better than BaseModel for data delivery~~
    - websocket for data delivery
        - combine BaseModel and msgpack for data delivery
- New node will force communicators to ping to UDP multicast group immediately, and wait for 1 seconds
    - during 1 seconds will receive all pongs
        - to acknowledge what communicators to keep up
    - force publisher to ping
        - receive pong from subscriber
    - force service client to ping
        - receive pong from service server
    - force action client to ping
        - receive pong from action server
    - once that ping peridiocally
- Topic matcher



