from picamera.array import PiRGBArray
from picamera import PiCamera
import socket
import time
import cv2
import numpy
import re
import serial
import threading

print('Start program')

port = serial.Serial("/dev/ttyUSB0", baudrate=115200)

def video_thread(): 
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

		rawCapture.truncate(0)
		cv2.waitKey(0)

def gamepad_thread():
	TCP_PORT_GAMEPAD = 9997
	BUFFER_SIZE = 64
	sock_gamepad = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_gamepad.bind(('', TCP_PORT_GAMEPAD))
	sock_gamepad.listen(1)
	conn_gamepad, addr = sock_gamepad.accept()
	print('Gamepad connected')
	while 1:
		data = conn_gamepad.recv(BUFFER_SIZE)
		if not data:
			continue
		result = ''
		for elem in data:
			result += str(int(elem))
			print(result)
			result += ' '
		result += '\n'
		print( result )
		port.write( result.encode() )


thread1 = threading.Thread(target=video_thread, args=())
thread2 = threading.Thread(target=gamepad_thread, args=())

thread1.daemon = True
thread2.daemon = True

thread1.start()
thread2.start()
thread1.join()
thread2.join()