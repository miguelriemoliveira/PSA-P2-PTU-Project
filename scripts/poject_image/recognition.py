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

with open('/home/joao/Desktop/PSA/PSA-P2-PTU-Project/scripts/poject_image/encodings.pickle', 'rb') as handle:
    knowledge= pickle.load(handle)

# Initialize webcam
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Find all faces in the current frame
    frame_detections = face_recognition.face_locations(frame)
    # print(frame_detections)
    frame_encodings = face_recognition.face_encodings(frame, frame_detections)
    # print(frame_encodings)


    # Match faces in current frame to known faces
    for frame_encoding, frame_detection in zip(frame_encodings, frame_detections):
        #  matches = face_recognition.compare_faces(knowledge['encodings'], frame_encoding,tolerance=0.2)
        #  print(matches)

        distances = face_recognition.face_distance(knowledge['encodings'], frame_encoding)
        print(distances)
        print(type(distances))
        print(distances.shape)

        summed_distances = []
        for distance in distances:
            summed_distances.append(sum(distance))
        print(summed_distances)

        idx_min= summed_distances.index(min(summed_distances))
        name= knowledge['labels'][idx_min]
        print('Recognized ' + name)

        
    
        # Draw box around face and label with name
        top, right, bottom, left = frame_detection
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()