import serial
import sys

serName = sys.argv[1]
ser = serial.Serial(serName, 115200)

while True:
    try:
        print(ser.readline())
    except:
        continue
