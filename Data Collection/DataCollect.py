import cv2
import numpy as np
import serial #Serial communication library
from time import sleep
import csv

ser= serial.Serial('/dev/ttyACM0',2400,timeout=0.5) #Serial communication between the arduino and the PC
ser.flushInput()
d=0
i=0 #i is the counter for the data added to the dataset

def make_resolution():
    #cap.set(3, 352)
    #cap.set(4, 240)
    cap.set(3, 480)
    cap.set(4, 360)
    #cap.set(3, 640)
    #cap.set(4, 480)

def rescale_frame(frame, percent=75):
    width = int(rows * percent/ 100)
    height = int(cols * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim)

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml') #load the face detection haarcascade model

cap= cv2.VideoCapture(0)
make_resolution() #fix the resolution you want
_, frame = cap.read()

rows,cols,_=frame.shape

sleep(2)
#with open('data_set.csv','w',newline='')as f: #This is when you want a new data_set to make
with open('data_set.csv','a',newline='')as f: #Adding data to the dataset data_set.csv
    thewriter=csv.writer(f)
    #thewriter.writerow(['x_resol','y_resol','w_values','h_values','target']) #this line is for making a new dataset
    while (i<300):
        print(d)
        #timer = cv2.getTickCount()
        ret, frame = cap.read()
        #frame=rescale_frame(frame, percent=50)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2)

        for (x, y, w, h) in faces:
            #print(x,y,w,h)
            ser_bytes = ser.readline() #read data from distance sensor in Arduino
            d=ser_bytes.decode().rstrip() #convert data
            thewriter.writerow([cols,rows,w,h,d]) #add data to the dataset
            i+=1
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y, x:x+w]

            Color = (0,0,255) #BGR not RGB !
            font=cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, "D="+ str(d), (x,y),font,0.4,Color,1, cv2.LINE_AA)
            width = x+w
            height = y+h
            #print(width,height)
            #print(x_med_cap,y_med_cap)
            cv2.rectangle(frame,(x,y),(width,height),Color,1)

        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        #cv2.putText(frame,"fps: " +str(int(fps)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
        cv2.imshow('Smile',frame)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

cap.release()
ser.close()
cv2.destroyAllWindows()
