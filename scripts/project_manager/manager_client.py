#!/usr/bin/env python3

import socket
from time import sleep
import json
import time
import numpy as np
import cv2 as cv

def main():

    # ---------------------------------------
    # Initialization
    # ---------------------------------------

    # Voice initialization
    voice_host = socket.gethostname() #as both code is running on same pc
    voice_port = 8080  #socket server port number
    voice_client_socket = socket.socket() #instantiate
    voice_client_socket.connect((voice_host,voice_port)) #connect to the server
    voice_messages = ['ola', 'bom dia', 'adeus']

    # Image initialization
    host = socket.gethostname() #as both code is running on same pc
    port = 8081  #socket server port number
    client_socket = socket.socket() #instantiate
    client_socket.connect((host,port)) #connect to the server
    message = {'request': 'empty'} #take input

    # ---------------------------------------
    # Execution
    # ---------------------------------------
    persons_in_scene = {}

    voice_message_idx = 0
    while True:

        client_socket.send(json.dumps(message).encode()) #send message
        data = (client_socket.recv(4098).decode()) #receive response
        print ('Received from server:  '+data) #show in terminal

        # convert message to sobjects dictionary
        sobjects = json.loads(data)

        for so in sobjects: # add a new person to the scene
            if not so['name'] in persons_in_scene:
                voice_message = 'bom dia ' + so['name']
                voice_client_socket.send(voice_message.encode()) #send message
                voice_response = voice_client_socket.recv(1024).decode() #receive response             
                persons_in_scene[so['name']] = {'stamp': time.time()}
            else:
                persons_in_scene[so['name']]['stamp'] = time.time()

        print(persons_in_scene)    
        # remove persons from scene
        keys_to_remove = []
        for person_in_scene_key, person_in_scene in persons_in_scene.items(): # add a new person to the scene
            delta = time.time() - person_in_scene['stamp']
            print(person_in_scene_key + ' was last seen ' + str(delta) + ' seconds ago')
            if delta > 10: # removing person from the scene if not seen for 10 secs
                keys_to_remove.append(person_in_scene_key)
                
        for key in keys_to_remove:
            del persons_in_scene[key]

        # Draw an image with the bboxes
        # create an empty image just to show the bboxes that we'll receive
        frame = np.zeros((480,640,3), dtype=np.uint8)        
        for so in sobjects:
            cv.rectangle(frame, (so['detection']['x'],so['detection']['y']), 
                            (so['detection']['x']+so['detection']['w'], 
                            so['detection']['y']+so['detection']['h']), (0,0,255), 3)
            cv.putText(frame, so['name'], (so['detection']['x'],so['detection']['y']-10), 
                        cv.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2) 
        
        cv.imshow('frame', frame)
        
        if cv.waitKey(20) == ord('q'):
            break

              

        # Send voice message
#         voice_message = 'Estou a ver o'
#         for so in sobjects:
#             voice_message += ' ' + so['name']
# 
#         voice_client_socket.send(voice_message.encode()) #send message
#         voice_response = voice_client_socket.recv(1024).decode() #receive response
# 
#         print('Received from server:  '+voice_response) #show in terminal

        sleep(0.1)


    # ---------------------------------------
    # Termination
    # ---------------------------------------
    voice_client_socket.close() #close connection
    client_socket.close() #close connection

if __name__ == "__main__":
    main()
