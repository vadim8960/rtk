from __future__ import print_function
import cv2
import time
import numpy
import socket
import xbox

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

frame_rate = 1
prev = 0


TCP_IP = '192.168.0.20'
TCP_PORT = 9997

print('Start gamepad');
joy = xbox.Joystick()

print('Start video stream')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
 
time.sleep(0.1)

print('Start main loop')
while 1:
	print('data sent')
	# length = recvall(s, 5)
	# print(length)
	# print('got length of image')
	# time.sleep(0.01)
	# stringData = recvall(s, int(length))
	# print(s.recv(3))
	# print('got picture')
	# data = numpy.fromstring(stringData, dtype='uint8')
	# decimg = cv2.imdecode(data,1)
	# ret, binary = cv2.threshold(decimg, 127, 255, cv2.THRESH_BINARY)

	buff = getDataFromGamepad(joy)

	time_elapsed = time.time() - prev
	prev = time.time()
	s.send(buff.encode());
	if (time_elapsed > 1./frame_rate):
		print(buff)
		
	# cv2.imwrite('~/image.jpg', decimg)
	# cv2.imshow('image',decimg) 
	# cv2.imshow('binary',binary) 
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break
