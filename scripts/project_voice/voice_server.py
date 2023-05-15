#!/usr/bin/env python3

# camera -> speak name -> S voice  == speaks

#teste voice input (name) => S Voice 


import socket  # Import socket module
from threading import Thread
# import argparse 

from gtts import gTTS
        
# This module is imported so that we can 
# play the converted audio
import os


def on_new_client(clientsocket,addr):
    """Launched to tackle the communication with every new client
    """

    while True: # Attending to the client's messages
        msg = clientsocket.recv(1024).decode()
        clientsocket.send('Message received'.encode())
        # Language in which you want to convert
        language = 'pt'
        
        tld="pt"

        # Passing the text and language to the engine, 
        # here we have marked slow=False. Which tells 
        # the module that the converted audio should 
        # have a high speed
        myobj = gTTS(text=msg, lang=language, tld=tld, slow=False)
        
        # Saving the converted audio in a mp3 file named
        # welcome 
        myobj.save("welcome.mp3")
        
        # Playing the converted file
        os.system("mpg321 welcome.mp3")


    clientsocket.close()

def main():
  

    # Configuration of parameters
    max_number_of_clients = 1
    number_connected_clients = 0

    # Initialization of socket communication
    my_socket = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 8080                # Reserve a port for your service.


    my_socket.bind((host, port))        # Bind to the port
    my_socket.listen(2)                 # Now wait for client connection.
    print('Server started!')
    print('Waiting for clients...')

    # Cycle attending to new client connection requests
    while True:         
        c, addr = my_socket.accept()     # Establish connection with client.

        if number_connected_clients == max_number_of_clients:
            c.close()
            print('Refused connection from ' + str(addr) + '. Too many clients.')
            continue

        print('Got connection from ' + str(addr))
        new_thread = Thread(target=on_new_client,args=(c,addr))
        new_thread.start()
        number_connected_clients += 1

    my_socket.close()

if __name__ == "__main__":
    main()


