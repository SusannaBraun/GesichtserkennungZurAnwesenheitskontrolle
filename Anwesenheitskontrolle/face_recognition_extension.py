import cv2
import face_recognition
import numpy as np

class profile_recognition():
    """description of class"""
    def __init__(self, encoded_images, file_names, video_cap):
        self.encoded_images = encoded_images
        self.file_names = file_names
        self.video_cap = video_cap

    def get_encoded_faces(self):
        success, img = self.video_cap.read()
        imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        return zip(encodesCurFrame, facesCurFrame), img

    def compare_face_with_list(self, encodeFace, faceLoc, img):
        matches = face_recognition.compare_faces(self.encoded_images, encodeFace)
        faceDis = face_recognition.face_distance(self.encoded_images, encodeFace)
        matchIndex = np.argmin(faceDis) 

        if matches[matchIndex]:
            name = self.file_names[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            cv2.rectangle(img, (x1,y1), (x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35), (x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2)
            return True, name
        return False

    def show_img(self, img):
        cv2.imshow('Webcam', img)
        cv2.waitKey(1)

    def exit(self):
        cv2.release()
        cv2.destroyAllWindows()


