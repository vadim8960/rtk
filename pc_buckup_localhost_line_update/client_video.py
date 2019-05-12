from __future__ import print_function
import cv2
import time
import numpy
import socket
import xbox
import threading

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: 
        	return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def video_thread():
	TCP_IP = '192.168.0.20'
	TCP_IP_LOCAL = '127.0.0.1'
	TCP_PORT_VIDEO = 9000

	sock_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_video.connect((TCP_IP, TCP_PORT_VIDEO))

	time.sleep(5)

	sock_local = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_local.connect((TCP_IP_LOCAL, 1924))

	kp = 1.5
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
		# blur = cv2.GaussianBlur(gray, (5, 5), 0)
		ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
		cv2.imshow('Bin', binary)
		dimen = binary.shape
		left  = 0
		right = 0
		start_left = 150
		end_left = 250
		start_right = 390
		end_right = 490
		# while (binary[300, it] > 0 and it < dimen[1] - 200):
		# 	left += 1
		# 	it += 1

		# it = dimen[1] - 200
		# while (binary[300, it] > 0 and it > 200):
		# 	right += 1
		# 	it -= 1

		for it in range(start_left, end_left):
			if (binary[410, it] == 0):
				left += 1

		for it in range(start_right, end_right):
			if (binary[410, it] == 0):
				right += 1

		error = (left - right)

		cv2.line(image, (start_left, 410), (end_left, 410), (255, 0, 0), 3)
		cv2.line(image, (start_right, 410), (end_right, 410), (255, 0, 0), 3)
		cv2.putText(image, str(left), (140, 410), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
		cv2.putText(image, str(error), (260, 410), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
		cv2.putText(image, str(right), (480, 410), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
		cv2.imshow('Original', image)

		p = kp * error
		i += (ki * error)
		d = kd * (error - error_old)
		u = int(p + i + d)
		sock_local.send((str(u) + '\n').encode())

		cv2.waitKey(1)



print('Start main loop')

thread1 = threading.Thread(target=video_thread, args=())
thread1.daemon = True
thread1.start()
thread1.join()
