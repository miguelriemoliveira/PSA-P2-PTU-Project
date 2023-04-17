#!/usr/bin/env python3

import numpy as np
import cv2 as cv
import os

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#image_dir = os.path.join(BASE_DIR,"faces")

#for root,dirs,files in os.walk(image_dir):
 #   for file in files:
  #      if file.endswith("png") or file.endswith("jpg"):
   #         path = os.path.join(root, file)
    #        print(path)







def main():
    cap = cv.VideoCapture(2) #TODO, verify if this value is correct in intel NUC
    print('Detecting people...')
    
    #pre-trained frontal face classifier
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

    if not cap.isOpened():
        print("Cannot open camera")
        exit()


    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        
        # Display the resulting frame
        
        #Detect faces present in the frame
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Draw a frame around the face of each detected person
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            iou_score= calculate_iou(box1, box2)
            cv.putText(frame, 'joao', (x,y-20), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1) #TODO create a way to compare real time image with photo
            cv.imshow('frame', frame)
       
        if cv.waitKey(1) == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
    