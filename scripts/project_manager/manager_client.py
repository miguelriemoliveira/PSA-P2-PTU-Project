#!/usr/bin/env python3

import socket
from time import sleep

def main():

    # ---------------------------------------
    # Initialization
    # ---------------------------------------
    voice_host = socket.gethostname() #as both code is running on same pc
    voice_port = 8080  #socket server port number

    voice_client_socket = socket.socket() #instantiate
    voice_client_socket.connect((voice_host,voice_port)) #connect to the server

    voice_messages = ['ola', 'bom dia', 'adeus']
    # ---------------------------------------
    # Execution
    # ---------------------------------------
    

    voice_message_idx = 0
    while True:

        if voice_message_idx > 2: # reset voice_message_idx
            voice_message_idx = 0
        voice_message = voice_messages[voice_message_idx]
        voice_message_idx += 1


        # Send voice message
        voice_client_socket.send(voice_message.encode()) #send message
        voice_response = voice_client_socket.recv(1024).decode() #receive response

        print('Received from server:  '+voice_response) #show in terminal

        sleep(2)


    # ---------------------------------------
    # Termination
    # ---------------------------------------
    voice_client_socket.close() #close connection

if __name__ == "__main__":
    main()
