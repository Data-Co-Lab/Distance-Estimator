import cv2
import numpy as np
from smbus import SMBus
import time
import RPi.GPIO as GPIO
import csv

addr=0x8
bus=SMBus(1)
ax=150
ay=75
ang=0
width1=360
height1=280
d=0
i=0
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
TRIG = 11
ECHO = 13
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def cal_dist():
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == False:
        start = time.time()
    while GPIO.input(ECHO)== True:
        end = time.time()
    sig_time = end-start
    distance = sig_time /  0.000058
    if distance>250:
        distance=0
    return(int (distance))

def make_resolution():
    cap.set(3, 1280) #480
    cap.set(4, 720)  #360

def encoded():
    bus.write_byte(addr, ay)
    return True

def rescale_frame(frame, percent=75):
    global width1
    global height1
    width1= int(frame.shape[1] * percent/ 100)
    height1= int(frame.shape[0] * percent/ 100)
    dim = (width1, height1)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

#Main
face_cascade = cv2.CascadeClassifier('/home/pi/FaceRec/src/Cascades/data/haarcascade_frontalface_alt2.xml')

cap= cv2.VideoCapture(0)
make_resolution()
_, frame = cap.read()
frame=rescale_frame(frame, percent=100)
rows,cols,_=frame.shape
time.sleep(0.5)
x_m= int(width1/2)
y_m= int(height1/2)
x_med_cap=x_m
y_med_cap=y_m

#with open('mydataTest.csv','w',newline='')as f:
with open('mydataTest.csv','a',newline='')as f:
    thewriter=csv.writer(f)
    #thewriter.writerow(['x_resol','y_resol','w_values','h_values','target'])
    while (i<200):

        ret, frame = cap.read()
        frame = cv2.flip(frame, 0)
        frame=rescale_frame(frame, percent=100)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2)

        for (x, y, w, h) in faces:
            #print(x,y,w,h)
            d=cal_dist()
            thewriter.writerow([width1,height1,w,h,ang,d])
            i+=1
            print(width1,height1,w,h,ang,d)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y, x:x+w]
            Color = (0,0,255) #BGR not RGB !
            font=cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, "D="+str(d), (x,y),font,0.4,Color,1, cv2.LINE_AA)

            width = x+w
            height = y+h
            #print(width,height)
            x_med_cap= int((x+x+w)/2)
            y_med_cap= int((y+y+h)/2)
            #print(x_med_cap," ",y_med_cap)
            cv2.rectangle(frame,(x,y),(width,height),Color,1)
        if cv2.waitKey(20) & 0xFF == ord('f'):
            break
        if x_med_cap < x_m-40:
            ax-=1
            if ax<90:
                ax=90
            #print("turn right")
        if x_med_cap > x_m+40:
            ax+=1
            if ax>180:
                ax=180
            #print("turn left")
        if y_med_cap < y_m-15:
            ay-=1
            if ay <10:
                ay=10

            #print("down it")
        if y_med_cap > y_m+15:
            ay+=1
            if ay > 100:
                ay=100
            #print("up it")
        #print(ay)
        encoded()
        ang=95-ay

        cv2.imshow('Face Detection',frame)


cap.release()
GPIO.cleanup()
cv2.destroyAllWindows()
