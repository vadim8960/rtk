from picamera.array import PiRGBArray
from picamera import PiCamera
import socket
import time
import cv2
import numpy
import re
import serial

prev = 0
frame_rate = 15

port = serial.Serial("/dev/ttyUSB0", baudrate=115200)

file = open('koef_pid.txt', 'r')
kp = float(file.readline())
ki = float(file.readline())
kd = float(file.readline())
file.close()

i = 0
error_old = 0
maxi = 0

TCP_IP = '0.0.0.0'
TCP_PORT = 9997
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', TCP_PORT))
s.listen(1)
conn, addr = s.accept()
print('Connection address:', addr)

camera = PiCamera()
camera.resolution = (640, 480)
#camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(640, 480))
# 240 x 320

print('get video')

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    u = 0
    time_elapsed = time.time() - prev
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if (time_elapsed > 1./frame_rate):
        prev = time.time()
        dimen = image.shape
        
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, imencode = cv2.imencode('.jpg', gray, encode_param)
        data = numpy.array(imencode)
        stringData = data.tostring()
        
        print("start translate: ", len(stringData))
        if (len(stringData) > 10000):
                conn.send(str(len(stringData)).encode())
                conn.send(stringData)
                conn.send('end'.encode());

        print('get data from gamepad')
        data_input = conn.recv(BUFFER_SIZE).decode()
        data_input = data_input.replace('\n', ' ')
        print('data got')

        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        left = 0
        right = 0
        
        iter = 0
        while (binary[300, iter] > 0 and iter < dimen[1] - 1):
            left += 1
            iter += 1

        iter = dimen[1] - 1
        while (binary[300, iter] > 0 and iter > 0):
            right += 1
            iter -= 1

        error = left - right

        p = kp * error
        i += (ki * error)
        d = kd * (error - error_old)

        u = int(p + i + d)

        rawCapture.truncate(0)

    #    for elem in data:
    #        result += str(elem)
    #        result += ' '
        data_input += (str(u) + ' ')
        data_input += '\n'
        print( data_input )
    #    port.write( result.encode() )
    #    trash = conn.recv(BUFFER_SIZE * 2)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    
s.close()
