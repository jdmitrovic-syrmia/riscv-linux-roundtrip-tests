#!/usr/bin/env python3

import serial
import subprocess
import getpass
import time
import sys

result = 1
uboot_path = sys.argv[2]

while result != 0:
    if result is None:
        continue
    result = subprocess.call(["boston", "flash", uboot_path])

print("U-Boot flash succesful.")

result = 1
bitfile_path = sys.argv[3]

while result != 0:
    if result is None:
        continue
    result = subprocess.call(["boston", "bitfile", bitfile_path])

port_name = "/dev/ttyUSB2"
baud_rate = 115200
ser = None

try:
    ser = serial.Serial(port_name, baud_rate, timeout=1)
    time.sleep(5) # Wait for device to initialize
    print("Connected to " + port_name)

    ser.flush()
    result = subprocess.call(["cpu_reset"])

    while True:
        line = ser.readline().decode('utf-8').strip()
        print("Received: " + line)
        if "login:" in line:
            data = input("Enter login:").encode("utf-8")
            ser.write(data + b'\r\n')
            ser.flush()
        elif "Password" in line:
            data = getpass.getpass().encode("utf-8")
            ser.write(data + b'\r\n')
            ser.flush()
            time.sleep(10)
            if ser.in_waiting:
                break
        time.sleep(0.01)

except serial.SerialException as e:
    print("Error opening serial port " + str(e))
except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    if ser and ser.is_open:
        ser.close()
        print("Serial port closed")
