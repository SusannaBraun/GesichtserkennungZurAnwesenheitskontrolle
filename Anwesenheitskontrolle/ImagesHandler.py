from base64 import encode
import os
from pathlib import Path
import cv2
import face_recognition
import Utilities

class Encoding():
    def __init__(self, path, debug = False):
        if(os.path.exists(path)):
            self.path = path
            self.images_folder = r'images'
            self.debug = debug
            self.encoded_images_file_name = r"Encoded_Images.txt"
            self.collected_names_file_name = r"Names.txt"
            if(not os.path.exists(path)):
                os.mkdir(os.path.join(self.path, self.images_folder))

        else:
            raise Exception(f'Path not found: {path}')

    def GetImages(self, path):
        if self.debug:
           print ("Getting Images!")
        imagesNames = []
        images = []
        myList = os.listdir(path)
        for cl in myList:
            if(os.path.exists(os.path.join(path, cl))):
               print (os.path.join(path, cl))
            curImg = cv2.imread(os.path.join(path, cl))#(f'{path}/{cl}')
            images.append(curImg)
            imagesNames.append(os.path.splitext(cl)[0])        
        if self.debug:
            print ("Success!")
        return images, imagesNames

    def GetImageEncoding(self, img):
        if self.debug:
            print ("start encoding img.")
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        if self.debug:
            print ("Success!")
        return encode

    def ConvertToEncodingList(self, images):
        encodeList = []
        if self.debug:
            print ("Converting Images to encoding list!")
        for img in images:
            try:
                encodeList.append(self.GetImageEncoding(img))
            except Exception as e:
                print("ErrorMessage: " + str(e))
        if self.debug:
                print ("Success!")
        return encodeList

    def collect_encoded_images_and_names(self):
        if(len(os.listdir(os.path.join(self.path, self.images_folder))) == 0):
            selected_path = Utilities.get_selected_path()
            images, fileNames = self.GetImages(selected_path)
            encodeList = self.ConvertToEncodingList(images)
            Utilities.WriteFile(encodeList, self.encoded_images_file_name, self.path)
            Utilities.WriteFile(fileNames, self.collected_names_file_name, self.path)
            Utilities.copy_all_files(selected_path, os.path.join(self.path, self.images_folder))

        elif (Utilities.dialog_yes_no("Ordner auswählen","Sollen neue Bilder hinzugefügt werden? (PS: es wird eine Kopie erstellt)")):
            fileNames = Utilities.ReadFile(self.collected_names_file_name, self.path)
            encodeList = Utilities.ReadFile(self.encoded_images_file_name, self.path)
            selected_path = Utilities.get_selected_path()
            newImages, newFileNames = self.GetImages(selected_path)
            fileNames = fileNames + newFileNames
            encodeList = encodeList + self.ConvertToEncodingList(newImages)
            Utilities.WriteFile(encodeList, self.encoded_images_file_name, self.path)
            Utilities.WriteFile(fileNames, self.collected_names_file_name, self.path)
            Utilities.copy_all_files(selected_path, os.path.join(self.path, self.images_folder))
        else:
            encodeList = Utilities.ReadFile(self.encoded_images_file_name, self.path)
            fileNames = Utilities.ReadFile(self.collected_names_file_name, self.path)
        return encodeList, fileNames