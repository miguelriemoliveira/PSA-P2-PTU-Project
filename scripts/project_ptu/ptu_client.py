#!/usr/bin/env python3

import socket
import json
import time

def main():
    host = socket.gethostname() #as both code is running on same pc
    port = 8080  #socket server port number

    client_socket = socket.socket() #instantiate
    client_socket.connect((host,port)) #connect to the server

    message = {'Pan':150 , 'Tilt':30} #take input

    while True:
        client_socket.send(json.dumps(message).encode()) #send message
        data = (client_socket.recv(1024).decode()) #receive response

        print ('Received from server:  '+data) #show in terminal

        if message == {'Pan':150 , 'Tilt':30}:
            time.sleep(1)
            message = {'Pan':-150 , 'Tilt':-30}

        elif message == {'Pan':-150, 'Tilt':-30}:
            time.sleep(1)
            message = {'Pan':150 , 'Tilt':30}


    client_socket.close() #close connection

if __name__ == "__main__":
    main()
