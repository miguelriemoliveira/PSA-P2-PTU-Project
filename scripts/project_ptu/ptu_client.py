#!/usr/bin/env python3

import socket
import json
import time

def main():
    host = socket.gethostname() #as both code is running on same pc
    port = 8082  #socket server port number

    client_socket = socket.socket() #instantiate
    client_socket.connect((host,port)) #connect to the server

    message = {'Pan':159 , 'Tilt':31} #take input

    while True:
        client_socket.send(json.dumps(message).encode()) #send message
        data = (client_socket.recv(1024).decode()) #receive response

        print ('Received from server:  '+data) #show in terminal

        if message == {'Pan':159 , 'Tilt':31}:
            time.sleep(10)
            message = {'Pan':-159 , 'Tilt':-47}

        elif message == {'Pan':-159, 'Tilt':-47}:
            time.sleep(10)
            message = {'Pan':159 , 'Tilt':31}


    client_socket.close() #close connection

if __name__ == "__main__":
    main()
