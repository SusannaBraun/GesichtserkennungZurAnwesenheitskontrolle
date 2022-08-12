import cv2
import numpy as np
import face_recognition

#Get images and turn them grey
imgEmilia = face_recognition.load_image_file(r"C:\UserData\z003yrpt\Documents\ProjektGesichtserkennung\VS\Anwesenheitskontrolle\images\emilia-clarke\1.jpg")
imgEmilia = cv2.cvtColor(imgEmilia,cv2.COLOR_BGR2RGB)
imgTest = face_recognition.load_image_file(r"C:\UserData\z003yrpt\Documents\ProjektGesichtserkennung\VS\Anwesenheitskontrolle\images\susanna-braun\4.jpg")
imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)

#Get face coordinates and draw a rectangle with those
faceLoc = face_recognition.face_locations(imgEmilia)[0]
encodeEmilia = face_recognition.face_encodings(imgEmilia)[0]
cv2.rectangle(imgEmilia, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255,0,255), 2)

#Get face coordinates and draw a rectangle with those
faceLoc = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255,0,255), 2)

results = face_recognition.compare_faces([encodeEmilia], encodeTest)
#the lower the distance the better the match
faceDis = face_recognition.face_distance([encodeEmilia], encodeTest)
print(results, faceDis)
cv2.putText(imgTest, f'{results} {round(faceDis[0], 2)}', (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2)


#Load the imgs
cv2.imshow('Emilia Clarke', imgEmilia)
cv2.imshow('Emilia Test', imgTest)
cv2.waitKey(0)