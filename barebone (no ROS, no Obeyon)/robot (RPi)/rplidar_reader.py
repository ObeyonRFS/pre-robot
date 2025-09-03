from rplidar import RPLidar
import ports_finder

# Change this to your port (e.g. "COM3" on Windows or "/dev/ttyUSB0" on Linux)
# PORT_NAME = '/dev/ttyUSB0'

ports = ports_finder.find_possible_RPLidar_ports()
if len(ports) != 1:
    raise SystemExit("ESP32 not found or too many devices")

PORT_NAME = ports[0]

lidar = RPLidar(PORT_NAME)


try:
    # Print some basic info
    info = lidar.get_info()
    print("LIDAR Info:", info)

    health = lidar.get_health()
    print("LIDAR Health:", health)

    lidar.start_motor()

    # Start scanning
    print("Starting scan...")
    for i, scan in enumerate(lidar.iter_scans()):
        print('%d: Got %d measurements' % (i, len(scan)))
        for (_, angle, distance) in scan:
            # angle in degrees, distance in mm
            print("Angle: %.2f°, Distance: %.1f mm" % (angle, distance))
        
        if i > 5:  # stop after 5 full scans
            break

finally:
    print("Stopping...")
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
