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
BUFFER_SIZE = 512

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', TCP_PORT))
s.listen(1)
conn, addr = s.accept()
print('Connection address:', addr)

print('get video')

time.sleep(0.1)

while 1:
    u = 0
    time_elapsed = time.time() - prev

    if (time_elapsed > 1./frame_rate):
        prev = time.time()


        print('get data from gamepad')
        data_input = conn.recv(BUFFER_SIZE).decode()
        data_input = data_input.replace('\n', ' ')
        print('data got')

        data_input += (str(u) + ' ')
        data_input += '\n'
        print( data_input )
        port.write( data_input.encode() )
    #    trash = conn.recv(BUFFER_SIZE * 2)

##    key = cv2.waitKey(1) & 0xFF
##    if key == ord("q"):
##        break
    
s.close()
