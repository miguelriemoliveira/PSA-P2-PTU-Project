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

def calculate_iou(box1, box2):
    # box1 and box2 are lists or tuples of [x, y, w, h] values
    
    # Get the coordinates of the top-left and bottom-right corners of each bounding box
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    x1_tl, y1_tl, x1_br, y1_br = x1, y1, x1 + w1, y1 + h1
    x2_tl, y2_tl, x2_br, y2_br = x2, y2, x2 + w2, y2 + h2
    
    # Calculate the coordinates of the intersection bounding box
    x_int_tl, y_int_tl = max(x1_tl, x2_tl), max(y1_tl, y2_tl)
    x_int_br, y_int_br = min(x1_br, x2_br), min(y1_br, y2_br)
    
    # Calculate the area of intersection
    if x_int_tl > x_int_br or y_int_tl > y_int_br:
        return 0.0 # no intersection
    else:
        int_area = (x_int_br - x_int_tl) * (y_int_br - y_int_tl)
    
    # Calculate the area of union
    box1_area = w1 * h1
    box2_area = w2 * h2
    union_area = box1_area + box2_area - int_area
    
    # Calculate the IOU score
    iou_score = int_area / union_area
    
    return iou_score




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
            iou_score= calculate_iou((x, y, w, h), (x, y, w, h))
            cv.putText(frame, 'joao', (x,y-20), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1) #TODO create a way to compare real time image with photo
            print(iou_score)
        cv.imshow('frame', frame)
       
        if cv.waitKey(1) == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
    