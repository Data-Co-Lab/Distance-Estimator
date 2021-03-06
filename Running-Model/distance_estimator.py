#import the needed libraries
import cv2
import numpy as np
import time
import pickle
import sklearn
from tensorflow.keras.models import load_model

estimator1 = pickle.load(open('Final_estimator.pickle', 'rb')) #Load the distance estimator model.
estimator=load_model('MLP_model.h5')
def Estimate(wid,hei):
    #preprocess the needed data for the ML model
    x_ratio=wid/cols
    y_ratio=hei/rows
    ed= estimator1.predict(np.array([[x_ratio,y_ratio]]))
    e_d= estimator.predict(np.array([[x_ratio,y_ratio]])) #predict the output as estimated distance
    return e_d,ed

def make_resolution():
    cap.set(3, 640)
    cap.set(4, 480)

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml') #load the face detection haarcascade model

cap= cv2.VideoCapture(0) #start the video feed from the cam
make_resolution() #fix the resolution you want
_, frame = cap.read() #initialise the frame from the video.

rows,cols,_=frame.shape #get the frame shape

while True:
    timer = cv2.getTickCount() #start counting the frame rate
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2) #the face detection parameters

    for (x, y, w, h) in faces:
        e_d,ed=Estimate(w,h) #Estimate the distance for every face in the frame
        e_d[0]=e_d[0]*220
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y, x:x+w]
        Color = (0,0,255) #BGR not RGB !
        font=cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "SVM D="+str(int(ed[0])), (x,y),font,0.6,(255,255,255),1, cv2.LINE_AA) #print the estimated distance on the frame
        cv2.putText(frame, "MLP D="+str(int(e_d[0])), (x,y-22),font,0.6,(255,255,255),1, cv2.LINE_AA)
        width = x+w
        height = y+h
        #print(width,height)
        #print(x_med_cap,y_med_cap)
        cv2.rectangle(frame,(x,y),(width,height),Color,1)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer) #get the frame rate
    cv2.putText(frame,"fps: " +str(int(fps)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2) #shows the frame rate on the corner of the frame
    cv2.imshow('Smile',frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
