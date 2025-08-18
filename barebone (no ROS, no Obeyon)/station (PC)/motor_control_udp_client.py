import asyncio
import json
import keyboard as kb

# --- Motor mapping ---
power_min = 100
power_max = 255

KEY_TO_MOTOR = {
    'w': {"L": 1, "R": 1},       # forward
    's': {"L": -1, "R": -1},     # backward
    'a': {"L": -0.5, "R": 0.5},  # turn left
    'd': {"L": 0.5, "R": -0.5},  # turn right
}


def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0


class UDPClientProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("✅ UDP client connected")

    def datagram_received(self, data, addr):
        print(f"⬅️ From server: {data.decode()}")


async def send_motor_commands(protocol: UDPClientProtocol, server_addr):
    prev_powerL, prev_powerR = None, None
    while True:
        if kb.is_pressed("q"):
            print("Exiting")
            break

        percentL = 0.0
        percentR = 0.0
        amplitude = 2/3

        if kb.is_pressed("up"):
            amplitude += 1/3
        if kb.is_pressed("down"):
            amplitude -= 1/3

        for key in KEY_TO_MOTOR:
            if kb.is_pressed(key):
                percentL += KEY_TO_MOTOR[key]["L"] * amplitude
                percentR += KEY_TO_MOTOR[key]["R"] * amplitude

        powerL, powerR = 0, 0
        if percentL != 0.0 or percentR != 0.0:
            powerL = sign(percentL) * int(power_min + (power_max - power_min) * abs(percentL))
            powerR = sign(percentR) * int(power_min + (power_max - power_min) * abs(percentR))

        if prev_powerL != powerL or prev_powerR != powerR:
            prev_powerL, prev_powerR = powerL, powerR

            message = {
                "command": "set_motor_power",
                "parameters": {"L": powerL, "R": powerR}
            }
            json_msg = json.dumps(message)
            protocol.transport.sendto(json_msg.encode(), server_addr)
            print(f"➡️ Sent: {message}")

        await asyncio.sleep(0.01)


async def main():
    loop = asyncio.get_running_loop()
    server_addr = ("urpi.local", 8765)  # replace with server IP or hostname

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPClientProtocol(),
        remote_addr=server_addr
    )

    try:
        await send_motor_commands(protocol, server_addr)
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())
