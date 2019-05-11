from __future__ import print_function
import cv2
import time
import socket
import numpy
import xbox
import threading
from queue import Queue

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

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: 
        	return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def video_thread(threadname, q):
	TCP_IP = '192.168.0.20'
	TCP_IP_LOCAL = '127.0.0.1'
	TCP_PORT_VIDEO = 9000

	sock_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_video.connect((TCP_IP, TCP_PORT_VIDEO))

	kp = 1
	ki = 0
	kd = 0
	i = 0
	error_old = 0

	print('Video start')
	while 1:
		length = recvall(sock_video, 5)
		stringData = recvall(sock_video, int(length))
		data = numpy.fromstring(stringData, dtype='uint8')
		image = cv2.imdecode(data,1)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
		cv2.imshow('Original', image)
		cv2.imshow('Bin', binary)

		dimen = binary.shape
		left  = 0
		right = 0
		it  = 0
		while (binary[50,it] > 0 and it < dimen[1] - 1):
			left += 1
			it += 1

		it = dimen[1] - 1
		while (binary[50,it] > 0 and it > 0):
			right += 1
			it -= 1

		error = left - right

		p = kp * error
		i += (ki * error)
		d = kd * (error - error_old)
		u = int(p + i + d)

		q.put(20)

		cv2.waitKey(1)

def gamepad_thread(threadname, q):
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
		u = q.get()
		buff.append(u)
		if (time_elapsed > 1./frame_rate):
			prev = time.time()
			print(buff)
			sock_gamepad.send(bytearray(buff))

queue = Queue()

thread1 = threading.Thread(target=video_thread, args=("Thread-1", queue))
thread2 = threading.Thread(target=gamepad_thread, args=("Thread-2", queue))
thread1.daemon = True
thread2.daemon = True
thread1.start()
thread2.start()
thread1.join()
thread2.join()