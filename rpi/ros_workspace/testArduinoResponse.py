import serial, time
s = serial.Serial('/dev/arduino', 115200, timeout = 2)
time.sleep(2)
s.write(b'<motor, 0, 0>\n')
time.sleep(0.5)
reply = s.read(200)
if reply:
	print('YES - arduino responded:', reply)
else:
	print('NO - arduino sent nothing back')

