from picamera.array import PiRGBArray
from picamera import PiCamera
import socket
import time
import cv2
import numpy

#port = serial.Serial("/dev/ttyUSB0", baudrate=115200)

file = open('koef_pid.txt', 'r')
kp = float(file.readline())
ki = float(file.readline())
kd = float(file.readline())
file.close()

TCP_IP = '0.0.0.0'
TCP_PORT = 9997
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', TCP_PORT))
s.listen(1)
conn, addr = s.accept()
print('Connection address:', addr)

frame_rate = 15
prev = 0
cap = cv2.VideoCapture(0)
# 480 x 640

print('get video')

time.sleep(0.1)



while 1:
    
    time_elapsed = time.time() - prev
    ret, image = cap.read()
    if (time_elapsed > 1./frame_rate):
        prev = time.time()
        dimen = image.shape
           
        image = image[140:(dimen[0] - 140), 220:(dimen[1] - 220)]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
        ret, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
            
       # cv2.imshow('image', binary)
        
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, imencode = cv2.imencode('.jpg', image, encode_param)
        data = numpy.array(imencode)
        stringData = data.tostring()
        
        print("start translate: ", len(stringData))

        conn.send(str(len(stringData)).encode()) #.ljust(16))
        conn.send(stringData)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
cap.release()
s.close()
