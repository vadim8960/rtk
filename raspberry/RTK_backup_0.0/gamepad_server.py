from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import socket
import re
import serial

port = serial.Serial("/dev/ttyUSB0", baudrate=115200)

TCP_IP = '0.0.0.0'
TCP_PORT = 9997
BUFFER_SIZE = 1024
line_mode = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen(1)
conn, addr = s.accept()
print('Connection address:', addr)

file = open('koef_pid.txt', 'r')
kp = float(file.readline())
ki = float(file.readline())
kd = float(file.readline())
file.close()

i = 0
error_old = 0
maxi = 0

width  = 656
heigth = 112

#camera = PiCamera()
#camera.resolution = (width, heigth)
#camera.framerate = 60
#rawCapture = PiRGBArray(camera, size=(width, heigth))

cap = cv2.VideoCapture(2)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#cap.set(cv2.CAP_PROR_FRAME_HEIGHT, heigth)

time.sleep(0.1)

while True:
	u = 0
	data = conn.recv(BUFFER_SIZE)
	if not data:
		continue
	result = ''
#	if line_mode:
	try:
		ret, image = cap.read()

		dimen = image.shape

		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

		#line  = image[50, : ]
		left  = 0
		right = 0

		iter  = 0
		while (image[50,iter] > 0 and iter < dimen[1] - 1):
			left += 1
			iter += 1

		iter = dimen[1] - 1
		while (image[50,iter] > 0 and iter > 0):
			right += 1
			iter -= 1

		error = left - right

		p = kp * error
		i += (ki * error)
		d = kd * (error - error_old)

		u = int(p + i + d)
	except AttributeError:
		u = 0

	for elem in data:
		result += str(elem)
		result += ' '
	if not line_mode:
		u = 0
	result += (str(u) + ' ')
	result += '\n'
	print( result )
	port.write( result.encode() )
	line_mode = data[4]
	trash = conn.recv(BUFFER_SIZE * 2)
