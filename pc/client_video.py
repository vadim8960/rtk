import cv2
import time
import numpy
import socket

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: 
        	return None
        buf += newbuf
        count -= len(newbuf)
    return buf

frame_rate = 1
prev = 0

TCP_IP = '192.168.0.20'
TCP_PORT = 9997

print('Start video stream')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
 
time.sleep(0.1)

print('Start main loop')
while 1:
	print('data sent')
	length = recvall(s, 5)
	print(length)
	print('got length of image')
	time.sleep(0.01)
	stringData = recvall(s, int(length))
	print('got picture')
	data = numpy.fromstring(stringData, dtype='uint8')
	image = cv2.imdecode(data,1)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

	cv2.imshow('Original', image)
	cv2.imshow('Bin', binary)

	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break