#!/usr/bin/env python3
import time
import serial
import json
import socket
from threading import Thread

def on_new_client(clientsocket,addr):
     
    print('defining serial')
    #define the serial connections
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=38400,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )
    
    print('serial defined')
     
    while True:
        msg = json.loads(clientsocket.recv(1024).decode())
        clientsocket.send('Message received'.encode())

        steps_pan = msg['Pan'] * 19
        steps_tilt = msg['Tilt'] * 19
        serial_input = f"pp{int(steps_pan)} tp{int(steps_tilt)}\n"
        ser.write(serial_input.encode())
        print('sending pan message')
        print(msg)

        out = ''

        while True:
            try: 
                print('Attempting to read')
                out += (ser.readline().decode())
                time.sleep(1)
                print(out)
                break

            except:
                pass

            ser.flush()

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



    serial_input = 'pp0\n'
    # Reading the data from the serial port (infinite loop)
    while 1:
        serial_input = input("")
        if serial_input == 'exit':
            ser.close()
            exit()
        else:
            serial_input += '\n'
            ser.write(serial_input.encode())
            out = ''

        time.sleep(1)
        while True:
            try: 
                print('Attempting to read')
                out += ser.readline().decode()
                time.sleep(1)
                print(out)
                break

            except:
                pass

        ser.flush()

if __name__ == "__main__":
    main()
