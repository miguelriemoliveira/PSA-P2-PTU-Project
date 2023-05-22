#!/usr/bin/env python3

# inpired in: https://www.mygreatlearning.com/blog/face-recognition/#face-recognition-using-python

import face_recognition
import cv2
import os
import pickle

# Load known faces and their names
known_faces = []
known_names = []
img_folder = '/home/joao/Desktop/PSA/PSA-P2-PTU-Project/scripts/poject_image/faces/'
class_folders= os.listdir(img_folder)
print(class_folders)

knowledge = {'encodings': [], 'labels': [], 'images': []}
for class_folder in class_folders:
    image_files= os.listdir(img_folder + class_folder)
    for image_file in image_files:
        filename = img_folder + class_folder + '/' + image_file
        print("Computing encodings for " + filename)
        img = face_recognition.load_image_file(filename)
        knowledge['images'].append(img)
        knowledge['encodings'].append(face_recognition.face_encodings(img))
        knowledge['labels'].append(class_folder)
 
#file_to_write = open("/home/joao/Desktop/PSA/PSA-P2-PTU-Project/scripts/poject_image/encodings.pickle", "wb")
file_to_write = open("encodings.pickle", "wb")
pickle.dump(knowledge, file_to_write)
