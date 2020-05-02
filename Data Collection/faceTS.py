import cv2
import numpy as np
import serial
from time import sleep
import RPi.GPIO as GPIO
import csv

ser= serial.Serial('/dev/ttyACM0',9600,timeout=1)
#ser.open()
xy=[]
ax=165
ay=110
d=0
i=0
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
TRIG = 11
ECHO = 13
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

ser.write(b'*')

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
    #cap.set(3, 480)
    #cap.set(4, 360)
    cap.set(3, 352)
    cap.set(4, 240)
def sendData():
    data=bytearray(xy)
    ser.write(data)
    #sleep(0.1)
    print(xy)

def encoded():
    a=str(ax)+','+str(ay)
    axy=bytes(a,'utf-8')
    ser.write(axy)
    print(axy)
    
def rescale_frame(frame, percent=75):
    width = int(rows * percent/ 100)
    height = int(cols * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim)

#print(ser.name)

face_cascade = cv2.CascadeClassifier('/home/pi/FaceRec/src/Cascades/data/haarcascade_frontalface_alt2.xml')
   
cap= cv2.VideoCapture(0)
make_resolution()
_, frame = cap.read()

rows,cols,_=frame.shape
#print(rows,cols)
x_m= int(cols/2)
y_m= int(rows/2)
print(x_m,y_m)
x_med_cap=x_m
y_med_cap=y_m
sleep(0.5)
ser.write(b'*')
sleep(0.5)
cv2.imshow('Smile',frame)
sleep(0.5)
print("Begin")
with open('mydataTest.csv','w',newline='')as f:
#with open('mydataTest.csv','a',newline='')as f:
    thewriter=csv.writer(f)
    thewriter.writerow(['x_resol','y_resol','w_values','h_values','target'])    
    while (i<200):

        timer = cv2.getTickCount()
        ret, frame = cap.read()
        frame = cv2.flip(frame, 0)
        #frame=rescale_frame(frame, percent=50)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2)
        
        for (x, y, w, h) in faces:
            #print(x,y,w,h)
            d=cal_dist()
            thewriter.writerow([cols,rows,w,h,ang,d])
            i+=1
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
            #print(x_med_cap,y_med_cap)
            cv2.rectangle(frame,(x,y),(width,height),Color,1)
        if x_med_cap < x_m-30:
            ax-=1
            if ax<100:
                ax=100
            
        if x_med_cap > x_m+30:
            ax+=1
            if ax>180:
                ax=180
            
        if y_med_cap < y_m-30:
            ay-=1
            if ay <70:
                ay=70
            
        if y_med_cap > y_m+30:
            ay+=1
            if ay > 130:
                ay=130
        
        xy=[ax,ay]
        sendData()
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        cv2.putText(frame,"fps: " +str(int(fps)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
        cv2.imshow('Smile',frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

GPIO.cleanup()
cap.release()
ser.close()
cv2.destroyAllWindows()
