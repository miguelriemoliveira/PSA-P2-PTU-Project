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

def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num

# def on_new_client(clientsocket,addr):
          
#     while True:
#         msg = json.loads(clientsocket.recv(1024).decode())
#         print('received ' + str(msg) )
#         clientsocket.send('Message received'.encode())

#     clientsocket.close()

def image_processing(cap, knowledge):

    print('image_processing ...')
    objects=[]
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

        print('image_processing ...')
        
        cv.imshow('frame', frame)

        if cv.waitKey(20) == ord('q'):
            break

        frame_count +=1


    #clientsocket.close()



def main():

    #open pickle file with known face encodings 
    with open('/home/joao/Desktop/PSA/PSA-P2-PTU-Project/scripts/poject_image/encodings.pickle', 'rb') as handle:
        knowledge= pickle.load(handle)

    cap = cv.VideoCapture(2) #TODO, verify if this value is correct in intel NUC
    print('opening camera...')
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # start a thread for image processing
    image_processing_thread = Thread(target=image_processing,args=(cap, knowledge))
    image_processing_thread.start()
    
    # Configuration of parameters
    # max_number_of_clients = 1
    # number_connected_clients = 0

    # # Initialization of socket communication
    # my_socket = socket.socket()         # Create a socket object
    # host = socket.gethostname() # Get local machine name
    # port = 8081             # Reserve a port for your service.

    # my_socket.bind((host, port))        # Bind to the port
    # my_socket.listen(2)                 # Now wait for client connection.
    # print('Server started!')
    # print('Waiting for clients...')

    # objects=[]
    # frame_count=0
    # object_count=0
    while True:
        continue
        #print('bla bla bla')
        # Handle new client connections
        # c, addr = my_socket.accept()     # Establish connection with client.
        # print('bla bla bla')
        # if number_connected_clients == max_number_of_clients:
        #     c.close()
        #     print('Refused connection from ' + str(addr) + '. Too many clients.')
        #     continue

        #print('Got connection from ' + str(addr))
        #new_thread = Thread(target=on_new_client,args=(c,addr))
        # new_thread.start()
        # number_connected_clients += 1

       # print('bla bla bla')



    # end of while
    
    #my_socket.close()

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
    