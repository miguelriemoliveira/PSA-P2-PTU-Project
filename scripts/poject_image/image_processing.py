#!/usr/bin/env python3

import numpy as np
import cv2 as cv
import os
import math
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#image_dir = os.path.join(BASE_DIR,"faces")

#for root,dirs,files in os.walk(image_dir):
 #   for file in files:
  #      if file.endswith("png") or file.endswith("jpg"):
   #         path = os.path.join(root, file)
    #        print(path)


#def calculate_iou(box1, box2):
    # box1 and box2 are lists or tuples of [x, y, w, h] values
    
    # Get the coordinates of the top-left and bottom-right corners of each bounding box
 #   x1, y1, w1, h1 = box1
  ###x2_tl, y2_tl, x2_br, y2_br = x2, y2, x2 + w2, y2 + h2
    
    # Calculate the coordinates of the intersection bounding box
 #   x_int_tl, y_int_tl = max(x1_tl, x2_tl), max(y1_tl, y2_tl)
 #   x_int_br, y_int_br = min(x1_br, x2_br), min(y1_br, y2_br)
    
    # Calculate the area of intersection
#    if x_int_tl > x_int_br or y_int_tl > y_int_br:
 #       return 0.0 # no intersection
  #  else:
   #     int_area = (x_int_br - x_int_tl) * (y_int_br - y_int_tl)
    
    # Calculate the area of union
    #box1_area = w1 * h1
    #box2_area = w2 * h2
    #union_area = box1_area + box2_area - int_area
    
    # Calculate the IOU score
    #iou_score = int_area / union_area
    
    #return iou_score 




def main():


    cap = cv.VideoCapture(2) #TODO, verify if this value is correct in intel NUC
    print('opening camera...')
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    #pre-trained frontal face classifier
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')


    objects=[]
    frame_count=0
    object_count=0
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        
        # Display the resulting frame
        
        #-------------------------------------
        #DETECTION 
        #-------------------------------------

        #Detect faces present in the frame
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Draw a frame around the face of each detected person
        count=0
        detections=[]
        for (x, y, w, h) in faces:
            detection= {'id': count,'x': x, 'y':y,'w':w,'h':h, 'frame':frame_count}
            detections.append(detection)
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #iou_score= calculate_iou((x), box2)
            cv.putText(frame, 'f ' + str(frame_count) + ' d ' + str(count), (x,y-20), 
                       cv.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1) #TODO create a way to compare real time image with photo

            count +=1

        #print(detections)

        #-------------------------------------
        #TRAKING
        #-------------------------------------
        def distance_centers(x1,y1,x2,y2):
            distance= math.sqrt((x1-x2)**2+(y1-y2)**2)
            return distance

            
        for detection in detections: #assciate detection to an object
            associated= False
            for o in objects:
                last_detection= o['detections'][-1]
                dist= distance_centers(detection['x'],detection['y'],
                                 last_detection['x'],last_detection['y'])

                if dist < 50:
                    o['detections'].append(detection)
                    associated=True
                    break

            if associated==False:

                # Create a objects for unassociated detections
                o={'id':object_count, 'detections': [detection]}
                objects.append(o)
                object_count+=1

        print('\n\n\n')
        print(objects)    

        #TODO object rectangle drawing

        #-------------------------------------
        #VISUALIZATIOM
        #-------------------------------------
        
        cv.imshow('frame', frame)


        if cv.waitKey(500) == ord('q'):
            break

        frame_count +=1

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
    