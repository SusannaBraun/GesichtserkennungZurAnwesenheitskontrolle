from base64 import encode
from ImagesHandler import Encoding
import Utilities
import cv2
import numpy as np
import face_recognition
import os
import shutil
from datetime import datetime
import pickle
import CsvHelper
import face_recognition_extension

base_path = r"C:\UserData\z003yrpt\Documents\ProjektGesichtserkennung\Anwesenheitskontrolle"
csv_file_name = r'attendance.csv'
imagesHandler = Encoding(base_path ,True)
encodeList, fileNames = imagesHandler.collect_encoded_images_and_names()
FaceRecognition = face_recognition_extension.profile_recognition(encodeList, fileNames, cv2.VideoCapture(0))
allNames = []

while True:
    encoded_faces, img = FaceRecognition.get_encoded_faces()
    for encodeFace, faceLoc in encoded_faces:
        success, profile_name = FaceRecognition.compare_face_with_list(encodeFace, faceLoc, img)
        if (success):
            if profile_name not in allNames:
                allNames = CsvHelper.markAttendance(profile_name, csv_file_name, base_path)

    FaceRecognition.show_img(img)
FaceRecognition.exit()