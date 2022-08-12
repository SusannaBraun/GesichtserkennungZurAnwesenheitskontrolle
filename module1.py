import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = r'C:\UserData\z003yrpt\Documents\ProjektGesichtserkennung\VS\Anwesenheitskontrolle\allimages'
images = []
classNames = []
myList = os.listdir(path)
#print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

#print(classNames)

def findEncoding(images, debug = False):
    encodeList = []
    if debug:
        print ("strarting sorting imges.")
    for img in images:
        try:
            encodeList.append(getImgEncoding(img, True))
        except Exception as e:
            print("ErrorMessage: " + str(e))
    if debug:
            print ("Success!")
    return encodeList


def getImgEncoding(img, debug = False):
        if debug:
            print ("start encoding img.")
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        
        if debug:
            print ("Success!")
        return encode
    

def markAttendance(name):
    with open(r'C:\UserData\z003yrpt\Documents\ProjektGesichtserkennung\VS\Anwesenheitskontrolle\attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        print(myDataList)
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')


        



encodeListKnown = findEncoding(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis) 

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            #y1, x2, y2, x1  =  y1*4, x2*4, y2*4, x1*4 
            cv2.rectangle(img, (x1,y1), (x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35), (x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2)
            markAttendance(name)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)


##Get face coordinates and draw a rectangle with those
#faceLoc = face_recognition.face_locations(imgEmilia)[0]
#encodeEmilia = face_recognition.face_encodings(imgEmilia)[0]
#cv2.rectangle(imgEmilia, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255,0,255), 2)

##Get face coordinates and draw a rectangle with those
#faceLoc = face_recognition.face_locations(imgTest)[0]
#encodeTest = face_recognition.face_encodings(imgTest)[0]
#cv2.rectangle(imgTest, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255,0,255), 2)

#results = face_recognition.compare_faces([encodeEmilia], encodeTest)
##the lower the distance the better the match
#faceDis = face_recognition.face_distance([encodeEmilia], encodeTest)
