from __future__ import print_function
import time
import socket
import xbox
import threading

def fmtFloat(n):
    return '{:6.3f}'.format(n)

def convertData(value):
	return int(100 * float(value))

def my_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def getDataFromGamepad(joy):
	buff = []
	buff.append(my_map(convertData(fmtFloat(joy.leftX())), -100, 100, 0, 254))
	buff.append(my_map(convertData(fmtFloat(joy.leftY())), -100, 100, 0, 254))
	buff.append(my_map(convertData(fmtFloat(joy.rightX())), -100, 100, 0, 254))
	buff.append(my_map(convertData(fmtFloat(joy.rightY())), -100, 100, 0, 255))
	buff.append(convertData(joy.A()) // 100)
	buff.append(convertData(joy.B()) // 100)
	buff.append(convertData(joy.X()) // 100)
	buff.append(convertData(joy.Y()) // 100)
	buff.append(convertData(joy.dpadUp()) // 100)
	buff.append(convertData(joy.dpadDown()) // 100)
	buff.append(convertData(joy.dpadLeft()) // 100)
	buff.append(convertData(joy.dpadRight()) // 100)
	buff.append(my_map(convertData(fmtFloat(joy.leftTrigger())), 0, 100, 0, 254))
	buff.append(my_map(convertData(fmtFloat(joy.rightTrigger())), 0, 100, 0, 254))
	return buff

def gamepad_thread():
	prev = 0
	frame_rate = 15
	TCP_IP = '192.168.0.20'
	TCP_IP_LOCAL = '127.0.0.1'
	TCP_PORT_GAMEPAD = 9997

	sock_gamepad = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_gamepad.connect((TCP_IP, TCP_PORT_GAMEPAD))

	joy = xbox.Joystick()
	print('Gamepad start')
	while 1:
		buff = getDataFromGamepad(joy)
		time_elapsed = time.time() - prev
		if (time_elapsed > 1./frame_rate):
			prev = time.time()
			print(buff)
			sock_gamepad.send(bytearray(buff))


thread2 = threading.Thread(target=gamepad_thread, args=())
thread2.daemon = True
thread2.start()
thread2.join()