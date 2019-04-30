import time
import cv2    

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


cap = cv2.VideoCapture(0)


time.sleep(0.1)

while 1:
    ret, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    dimen = image.shape
    
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    
    cv2.imshow('image', image)
    
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
    
    u = p + i + d
    
    print(50 + u, ' ', 50 - u)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()