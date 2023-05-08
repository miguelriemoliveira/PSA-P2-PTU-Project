#!/usr/bin/env python3

import numpy as np
import cv2 as cv
import os
import math
import time
import face_recognition
import pickle

def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num


def main():

    #open pickle file with known face encodings 
    with open('/home/joao/Desktop/PSA/PSA-P2-PTU-Project/scripts/poject_image/encodings.pickle', 'rb') as handle:
        knowledge= pickle.load(handle)



    cap = cv.VideoCapture(2) #TODO, verify if this value is correct in intel NUC
    print('opening camera...')
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # #pre-trained frontal face classifier
    # face_cascade = cv.CascadeClassifier('/home/joao/Desktop/PSA/PSA-P2-PTU-Project/scripts/poject_image/haarcascade_frontalface_default.xml')


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
        #frame_detections = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Find all faces in the current frame
        frame_detections = face_recognition.face_locations(frame)
        # print(frame_detections)
        frame_encodings = face_recognition.face_encodings(frame, frame_detections)

        count=0
        detections=[]
        # Build list of detections and match faces in current frame to known faces
        for frame_encoding, frame_detection in zip(frame_encodings, frame_detections):
           
            distances = face_recognition.face_distance(knowledge['encodings'], frame_encoding)
           
            summed_distances = []
            for distance in distances:
                summed_distances.append(sum(distance))

            idx_min= summed_distances.index(min(summed_distances))
            name= knowledge['labels'][idx_min]

            # Build list of detections
            top, right, bottom, left = frame_detection
            x,y,w,h = left, top, right-left, bottom-top
            xc= int(x+w/2)
            yc= int(y+h/2)
            detection= {'id': count,'x': x, 'y':y,'w':w,'h':h, 'frame':frame_count, 
                        'stamp':time.time(),'name':name,'xc':xc,'yc':yc}
            detections.append(detection)
            count +=1


        #-------------------------------------
        #TRAKING
        #-------------------------------------

        def distance_centers(x1,y1,x2,y2):
            distance= math.sqrt((x1-x2)**2+(y1-y2)**2)
            return distance
            
        for detection in detections: #assciate detection to an object
            associated= False
            for o in objects:
                if not o['active']:
                    continue

                last_detection= o['detections'][-1]
                dist= distance_centers(detection['x'],detection['y'],
                                 last_detection['x'],last_detection['y'])

                if dist < 50:
                    o['detections'].append(detection)
                    associated=True
                    break

            if associated==False:

                # Create a objects for unassociated detections
                o={'id':object_count, 'detections': [detection], 'active': True,
                   'name':'unkown'}
                objects.append(o)
                object_count+=1 

        # Update object person recognition
        # We will use the majority of the recognitions of the detections of that object
        for o in objects:
            names=[]
            for detection in o['detections']:
                names.append(detection['name'])
                
            o['name']=most_frequent(names)

 
        


        #update active objects
        for o in objects:
            detection= o['detections'][-1]
            elapsed_time = time.time() - detection['stamp']
            if elapsed_time > 3 :
                o['active']= False


        #-------------------------------------
        #VISUALIZATIOM
        #-------------------------------------
        
        #Draw all objects
        for o in objects:
            if not o['active']:
                continue

            detection= o['detections'][-1]
            cv.rectangle(frame, (detection['x'],detection['y']), 
                         (detection['x']+detection['w'], 
                          detection['y']+detection['h']), (0,0,255), 3)
            text = 'o' + str(o['id']) + ' ' + o['name']
            cv.putText(frame, text, (detection['x'],detection['y']-10), 
                       cv.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2) 

        #Draw all detections
        for detection_idx, detection in enumerate(detections):
            cv.rectangle(frame, (detection['x'],detection['y']),
                          (detection['x']+detection['w'],
                            detection['y']+detection['h']), (0, 255, 0), 1)
            cv.putText(frame, 'f ' + str(frame_count) + ' d ' + str(detection_idx),
                        (detection['x'],detection['y']-20), 
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
    