from rplidar import RPLidar
import ports_finder

ports = ports_finder.find_possible_RPLidar_ports()
if len(ports) != 1:
    raise SystemExit("ESP32 not found or too many devices")

PORT_NAME = ports[0]

lidar = RPLidar(PORT_NAME, baudrate=115200)

lidar.start_motor()

print('Info:', lidar.get_info())
print('Health:', lidar.get_health())

for i, measurement in enumerate(lidar.iter_measurments()):
    quality, angle, distance = measurement
    print(f"Q={quality}, Angle={angle:.2f}, Dist={distance:.1f} mm")
    if i > 50:
        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
