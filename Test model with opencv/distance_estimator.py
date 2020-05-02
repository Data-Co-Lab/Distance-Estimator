import cv2
import numpy as np
import time
import pickle
#from sklearn import svm
import sklearn
#from sklearn.linear_model import LinearRegression

estimator = pickle.load(open('Final_estimator.pickle', 'rb'))
def Estimate(wid,hei):
    x_ratio=wid/cols
    y_ratio=hei/rows

    e_d= estimator.predict(np.array([[x_ratio,y_ratio]]))
    return e_d

def make_resolution():
    cap.set(3, 640)
    cap.set(4, 480)

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')

cap= cv2.VideoCapture(0)
make_resolution()
_, frame = cap.read()

rows,cols,_=frame.shape
#print(rows,cols)

while True:
    timer = cv2.getTickCount()
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2)

    for (x, y, w, h) in faces:
        #print(x,y,w,h)
        ed=Estimate(w,h)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y, x:x+w]
        Color = (0,0,255) #BGR not RGB !
        font=cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "Estimated D="+str(int(ed[0])), (x,y),font,0.6,(255,255,255),1, cv2.LINE_AA)
        width = x+w
        height = y+h
        #print(width,height)
        #print(x_med_cap,y_med_cap)
        cv2.rectangle(frame,(x,y),(width,height),Color,1)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(frame,"fps: " +str(int(fps)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
    cv2.imshow('Smile',frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()