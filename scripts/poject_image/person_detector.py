#!/usr/bin/env python3

import numpy as np
import cv2 as cv
import os
import math
import time
import face_recognition
import pickle
import socket
from threading import Thread
import json
from copy import deepcopy

maximum_distance_for_association = 300
time_to_turn_innactive = 1

objects=[] # global variable to be accecible by two functions
 
def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num

def on_new_client(clientsocket,addr):
    global objects

    while True:
        msg = json.loads(clientsocket.recv(1024).decode())
        print('received request')

        # Create a dictionary of tracked persons to send
        # lets call it a simplified objects or sobjects

        sobjects = []
        for o in objects:
            if not o['active']: # skip non active objects
                continue

            so = deepcopy(o)
            so['detection'] = so['detections'][-1]
            del so['detections']
            sobjects.append(so)

        # send the simplified version sobjects
        clientsocket.send(json.dumps(sobjects).encode())
        

    clientsocket.close()

def image_processing(clientsocket, cap, knowledge):

    global objects
    global time_to_turn_innactive
    global maximum_distance_for_association
   
    frame_count=0
    object_count=0
    while True:
        # Process image
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # print('image_processing ...')
        
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

                # associate detection with object
                if dist < maximum_distance_for_association and detection['name'] == o['name']:
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
            if elapsed_time >  time_to_turn_innactive:
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


    clientsocket.close()



def main():

    #open pickle file with known face encodings 
    with open('/home/joao/Desktop/PSA/PSA-P2-PTU-Project/scripts/poject_image/encodings.pickle', 'rb') as handle:
        knowledge= pickle.load(handle)

    cap = cv.VideoCapture(2) #TODO, verify if this value is correct in intel NUC
    print('opening camera...')
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # Configuration of parameters
    max_number_of_clients = 1
    number_connected_clients = 0

    # Initialization of socket communication
    my_socket = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 8081             # Reserve a port for your service.

    # start a thread for image processing
    image_processing_thread = Thread(target=image_processing,args=(my_socket, cap, knowledge))
    image_processing_thread.start()


    my_socket.bind((host, port))        # Bind to the port
    my_socket.listen(2)                 # Now wait for client connection.
    print('Server started!')
    print('Waiting for clients...')

    
    while True:
        # Handle new client connections
        c, addr = my_socket.accept()     # Establish connection with client.
        if number_connected_clients == max_number_of_clients:
            c.close()
            print('Refused connection from ' + str(addr) + '. Too many clients.')
            continue

        print('Got connection from ' + str(addr))
        new_thread = Thread(target=on_new_client,args=(c,addr))
        new_thread.start()
        number_connected_clients += 1

    # end of while
    
    my_socket.close()

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
    