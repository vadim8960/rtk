from picamera.array import PiRGBArray
from picamera import PiCamera
import socket
import time
import cv2
import numpy
import re
import serial
import threading
from queue import Queue

print('Start program')

port = serial.Serial("/dev/ttyUSB0", baudrate=115200)

file = open('koef_pid.txt', 'r')
kp = float(file.readline())
ki = float(file.readline())
kd = float(file.readline())
file.close()

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
	TCP_PORT_VIDEO = 9000
	sock_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_video.bind(('', TCP_PORT_VIDEO))
	sock_video.listen(1)
	conn_video, addr = sock_video.accept()
	print('Video connected')
	prev = 0
	frame_rate = 15
	camera = PiCamera()
	camera.resolution = (640, 480)
	rawCapture = PiRGBArray(camera, size=(640, 480))
	print('Camera connected')
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		time_elapsed = time.time() - prev
		if (time_elapsed > 1./frame_rate):
			image = frame.array
			prev = time.time()
			encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
			result, imencode = cv2.imencode('.jpg', image, encode_param)
			data = numpy.array(imencode)
			stringData = data.tostring()
			# print("start translate: ", len(stringData))

			if (len(stringData) > 10000):
				conn_video.send(str(len(stringData)).encode())
				conn_video.send(stringData)


		raw_data = list(recvall(conn_video, 1))
		q.put(raw_data[0])

		rawCapture.truncate(0)
		cv2.waitKey(0)

def gamepad_thread(threadname, q):
	TCP_PORT_GAMEPAD = 9997
	BUFFER_SIZE = 1024
	sock_gamepad = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_gamepad.bind(('', TCP_PORT_GAMEPAD))
	sock_gamepad.listen(1)
	conn_gamepad, addr = sock_gamepad.accept()
	u = 0
	print('Gamepad connected')
	while 1:
		data = recvall(conn_gamepad, 14)
		recvall(conn_gamepad, 3 * 14)
		if not data:
			continue
		result = ''
		for elem in data:
			result += str(int(elem))
			result += ' '
		u = q.get()
		if not data[4]:
			u = 0
		result += (str(u) + ' ')
		result += '\n'
		print( result )
		port.write( result.encode() )

queue = Queue()

thread1 = threading.Thread(target=video_thread, args=("Thread-1", queue))
thread2 = threading.Thread(target=gamepad_thread, args=("Thread-2", queue))

thread1.daemon = True
thread2.daemon = True

thread1.start()
thread2.start()
thread1.join()
thread2.join()