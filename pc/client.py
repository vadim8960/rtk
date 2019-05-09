from __future__ import print_function
import cv2
import time
import numpy
import socket
import xbox
import threading
import os
import pwd

os.seteuid(pwd.getpwnam(os.getlogin()).pw_uid)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: 
        	return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def fmtFloat(n):
    return '{:6.3f}'.format(n)

def convertData(value):
	return int(100 * float(value))

def my_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def getDataFromGamepad(joy):
	buff = ''
	buff += (str(my_map(convertData(fmtFloat(joy.leftX())), -100, 100, -255, 255)) + ' ')
	buff += (str(my_map(convertData(fmtFloat(joy.leftY())), -100, 100, -255, 255)) + ' ')
	buff += (str(my_map(convertData(fmtFloat(joy.rightX())), -100, 100, -255, 255)) + ' ')
	buff += (str(my_map(convertData(fmtFloat(joy.rightY())), -100, 100, -255, 255)) + ' ')
	buff += (str(convertData(joy.A())) + ' ')
	buff += (str(convertData(joy.B())) + ' ')
	buff += (str(convertData(joy.X())) + ' ')
	buff += (str(convertData(joy.Y())) + ' ')
	buff += (str(convertData(joy.dpadUp())) + ' ')
	buff += (str(convertData(joy.dpadDown())) + ' ')
	buff += (str(convertData(joy.dpadLeft())) + ' ')
	buff += (str(convertData(joy.dpadRight())) + ' ')
	buff += (str(my_map(convertData(fmtFloat(joy.leftTrigger())), 0, 100, 0, 255)) + ' ')
	buff += (str(my_map(convertData(fmtFloat(joy.rightTrigger())), 0, 100, 0, 255)) + '\n')
	return buff

def video_thread():
	TCP_IP = '192.168.0.20'
	TCP_PORT_VIDEO = 9000
	sock_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_video.connect((TCP_IP, TCP_PORT_VIDEO))
	os.seteuid(0)
	print('Video start')
	while 1:
		# print('data sent')
		length = recvall(sock_video, 5)
		# print(length)
		# print('got length of image')
		stringData = recvall(sock_video, int(length))
		# print('got picture')
		data = numpy.fromstring(stringData, dtype='uint8')
		image = cv2.imdecode(data,1)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
		print('Start draw')
		cv2.imshow('Original', image)
		# cv2.imshow('Bin', binary)
		cv2.waitKey(1)
		print('End draw')

def gamepad_thread():
	prev = 0
	frame_rate = 10
	TCP_IP = '192.168.0.20'
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
			sock_gamepad.send(buff.encode())


print('Start main loop')

thread1 = threading.Thread(target=video_thread, args=())
thread2 = threading.Thread(target=gamepad_thread, args=())

thread1.daemon = True
thread2.daemon = True

thread1.start()
thread2.start()
thread1.join()
thread2.join()