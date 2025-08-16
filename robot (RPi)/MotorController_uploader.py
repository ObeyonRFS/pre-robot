import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change working directory to that
os.chdir(script_dir)
os.chdir("MotorController")
os.chdir("build/esp32.esp32.esp32da")
os.system("esptool --chip esp32 --port /dev/ttyUSB1 --baud 921600 write_flash -z 0x1000 .\MotorController.ino.bootloader.bin 0x8000 .\MotorController.ino.partitions.bin 0x10000 .\MotorController.ino.bin")