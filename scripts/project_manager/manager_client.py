#!/usr/bin/env python3

import random
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
    
    W = 320
    H = 240
    deg_per_pixel = 60.0/W
    kp = 0.5

    # Voice initialization
    voice_host = socket.gethostname() #as both code is running on same pc
    voice_port = 8080  #socket server port number
    voice_client_socket = socket.socket() #instantiate
    voice_client_socket.connect((voice_host,voice_port)) #connect to the server

    # Image initialization
    image_host = socket.gethostname() #as both code is running on same pc
    image_port = 8081  #socket server port number
    image_client_socket = socket.socket() #instantiate
    image_client_socket.connect((image_host,image_port)) #connect to the server
    image_message = {'request': 'empty'} #take input

    # PTU initialization
    host = socket.gethostname() #as both code is running on same pc
    port = 8082  #socket server port number

    client_socket = socket.socket() #instantiate
    client_socket.connect((host,port)) #connect to the server



    # ---------------------------------------
    # Execution
    # ---------------------------------------
    persons_in_scene = {}
    following_person = ''


    # Voice options
    voice_message_idx = 0
    hello_options = ['Bom dia ', 'Olá ', 'Tudo bem ', 'Oi ', 'Olha o ', 'Estou te a ver ', 'Boas ']
    following_options = ['Estou a seguir-te ', 'Anda cá ', 'Vou atrás de ti ', 'Não fujas ', 'Vou te apanhar ']
    goodbye_options = ['Xauzão ', 'Adeus ', 'Até à próxima ', 'Volte sempre ', 'Fica bem ']

    while True:

        image_client_socket.send(json.dumps(image_message).encode()) #send message
        data = (image_client_socket.recv(4098).decode()) #receive response
        print ('Received from server:  '+data) #show in terminal

        # convert message to sobjects dictionary
        sobjects = json.loads(data)

        for so in sobjects: # add a new person to the scene
            if not so['name'] in persons_in_scene:
                if so['name'] != 'unknown person':
                    voice_message = hello_options[random.randint(0,len(hello_options)-1)] + so['name'] 
                    voice_client_socket.send(voice_message.encode()) #send message
                    # voice_response = voice_client_socket.recv(1024).decode() #receive response

            persons_in_scene[so['name']] = {'stamp': time.time()}
            if following_person == '' and so['name'] != 'unknown person':
                following_person=so['name']
                voice_message = following_options[random.randint(0,len(following_options)-1)] + so['name'] 
                voice_client_socket.send(voice_message.encode()) #send message
                        # voice_response = voice_client_socket.recv(1024).decode() #receive response
            else:
                persons_in_scene[so['name']]['stamp'] = time.time()


        print('i am following ' + following_person)
       
        # remove persons from scene
        keys_to_remove = []
        for person_in_scene_key, person_in_scene in persons_in_scene.items(): # add a new person to the scene
            delta = time.time() - person_in_scene['stamp']
            print(person_in_scene_key + ' was last seen ' + str(delta) + ' seconds ago')
            if delta > 3: # removing person from the scene if not seen for 3 secs
                keys_to_remove.append(person_in_scene_key)
                
        for key in keys_to_remove:
            del persons_in_scene[key]
            if following_person == key:
                following_person = ''
                
                voice_message = goodbye_options[random.randint(0,len(goodbye_options)-1)] + key 
                voice_client_socket.send(voice_message.encode()) #send message
                voice_response = voice_client_socket.recv(1024).decode() #receive response

        
        #PTU execution

        #find center of followed person
        center_x = None
        center_y = None
        for so in sobjects: # add a new person to the scene
            if following_person == so['name']:
                center_x = so['detection']['xc']
                center_y = so['detection']['yc'] 
                break

        #convert center to degrees
        if center_x is None:
            deg_x = 0
            deg_y = 0
        else:
            deg_x = -(center_x - W/2)* deg_per_pixel * kp
            deg_y = 0

            message = {'Pan':deg_x , 'Tilt': deg_y} #take input
            client_socket.send(json.dumps(message).encode()) #send message
            data = (client_socket.recv(1024).decode()) #receive response

        # print ('Received from server:  '+data) #show in terminal


        # Draw an image with the bboxes
        # create an empty image just to show the bboxes that we'll receive
        frame = np.zeros((H,W,3), dtype=np.uint8)        
        for so in sobjects:
            cv.rectangle(frame, (so['detection']['x'],so['detection']['y']), 
                            (so['detection']['x']+so['detection']['w'], 
                            so['detection']['y']+so['detection']['h']), (0,0,255), 3)
            cv.putText(frame, so['name'], (so['detection']['x'],so['detection']['y']-10), 
                        cv.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2) 
        
        #escrever um texto a dizer quem estou a seguir
        cv.putText(frame, 'i am following ' + following_person, (30,200), 
                    cv.FONT_HERSHEY_PLAIN, 1, (255,0,255), 2) 
        cv.imshow('frame', frame)
        
        if cv.waitKey(20) == ord('q'):
            break
        

              

        sleep(0.1)


    # ---------------------------------------
    # Termination
    # ---------------------------------------
    voice_client_socket.close() #close connection
    image_client_socket.close() #close connection

if __name__ == "__main__":
    main()
