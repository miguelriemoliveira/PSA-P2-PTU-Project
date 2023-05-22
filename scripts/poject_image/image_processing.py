#!/usr/bin/env python3

import numpy as np
import cv2 as cv
import os
import math


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
        cv.imshow('test',gray)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)


        # Build list of detections
        count=0
        detections=[]
        for (x, y, w, h) in faces:
            detection= {'id': count,'x': x, 'y':y,'w':w,'h':h, 'frame':frame_count}
            detections.append(detection)
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

        # print('\n\n\n')
        # print(objects)    

        #TODO object rectangle drawing

        #-------------------------------------
        #VISUALIZATIOM
        #-------------------------------------
        
        

        #Draw all objects
        for o in objects:
            detection= o['detections'][-1]
            cv.rectangle(frame, (detection['x'],detection['y']), (detection['x']+detection['w'], detection['y']+detection['h']), (0,0,255), 3)
            cv.putText(frame, 'o ' + str(o['id']), (detection['x'],detection['y']-10), 
                       cv.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2) 

        #Draw all detections
        for detection_idx, detection in enumerate(detections):
            cv.rectangle(frame, (detection['x'],detection['y']), (detection['x']+detection['w'], detection['y']+detection['h']), (0, 255, 0), 1)
            cv.putText(frame, 'f ' + str(frame_count) + ' d ' + str(detection_idx), (detection['x'],detection['y']-20), 
                       cv.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2) 


        cv.imshow('frame', frame)


        if cv.waitKey(20) == ord('q'):
            break

        frame_count +=1

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
    