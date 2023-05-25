#!/usr/bin/env python3

import socket
import json
import time
import numpy as np
import cv2 as cv

def main():
    host = socket.gethostname() #as both code is running on same pc
    port = 8081  #socket server port number

    client_socket = socket.socket() #instantiate
    client_socket.connect((host,port)) #connect to the server

    message = {'request': 'empty'} #take input

   
    while True:
        client_socket.send(json.dumps(message).encode()) #send message
        data = (client_socket.recv(4098).decode()) #receive response
        print ('Received from server:  '+data) #show in terminal

        # convert message to sobjects dictionary
        sobjects = json.loads(data)

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
        
        time.sleep(1)

    client_socket.close() #close connection

if __name__ == "__main__":
    main()
