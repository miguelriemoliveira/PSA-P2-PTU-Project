#!/usr/bin/env python3
from functools import partial
import signal
import time
import serial
import json
import socket
from threading import Thread


def handler(signal_received, frame, serial):
    """
    Signal handler function for safely closing the script.

    Parameters:
        signal_received (int): The signal number or code.
        frame (frame object): The current stack frame.
        serial: A serial object used for communication.

    Returns:
        None

    Raises:
        None

    """
    print('Safely closing the script')
    serial_input = 'tp0 pp0\n'
    serial.write(serial_input.encode())
    print('Safely closed')
    exit(0)

    

def map_value(value, in_min, in_max, out_min, out_max):
    # Normalize the input value
    normalized_value = (value - in_min) / (in_max - in_min)
    
    # Map the normalized value to the output range
    mapped_value = normalized_value * (out_max - out_min) + out_min
    
    return mapped_value


def on_new_client(clientsocket, addr, ser):
    """
    Function to handle a new client connection.

    Parameters:
        clientsocket (socket object): The client socket for communication.
        addr (tuple): The client address (IP address, port number).
        ser: A serial object used for communication.

    Returns:
        None

    Raises:
        None

    """
    # Define step and angle ranges for pan and tilt
    min_steps_pan = -10416
    max_steps_pan = 10416
    min_angle_pan = -159
    max_angle_pan = 159
    min_steps_tilt = -6000
    max_steps_tilt = 3000
    min_angle_tilt = -47
    max_angle_tilt = 31

    pan_sa = (max_steps_pan - min_steps_pan)/(max_angle_pan - min_angle_pan)
    tilt_sa = (max_steps_tilt - min_steps_tilt)/(max_angle_tilt - min_angle_tilt)


    while True:
        # Receive and process messages from the client
        msg = json.loads(clientsocket.recv(1024).decode())
        clientsocket.send('Message received'.encode())

        # Map angle values to steps based on defined ranges
        #steps_pan = map_value(msg['Pan'], min_angle_pan, max_angle_pan, min_steps_pan, max_steps_pan)
        #steps_tilt = map_value(msg['Tilt'], min_angle_tilt, max_angle_tilt, min_steps_tilt, max_steps_tilt)
        steps_pan = map_value(msg['Pan']) * pan_sa
        steps_tilt = map_value(msg['Tilt']) * tilt_sa

        # Construct and send the serial command
        serial_input = f"po{int(steps_pan)} to{int(steps_tilt)}\n"
        print(serial_input)
        ser.write(serial_input.encode())
        print('Sending pan message')
        print(msg)

        out = ''

        # Read serial output from the device
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

    # Close the client socket
    clientsocket.close()

def main():
    # Configuration of parameters
    max_number_of_clients = 1
    number_connected_clients = 0

    print('Defining serial connection')
    # Define the serial connection
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=38400,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    # Initialize the serial connection
    ser.write('RP\n'.encode())
    time.sleep(15)
    print('Serial connection defined')

    # Define a signal handler for safe script termination
    handler_partial = partial(handler, serial=ser)
    signal.signal(signal.SIGINT, handler_partial)

    # Initialization of socket communication
    my_socket = socket.socket()                 # Create a socket object
    host = socket.gethostname()                  # Get local machine name
    port = 8082                                  # Reserve a port for the service.

    my_socket.bind((host, port))                  # Bind to the port
    my_socket.listen(2)                           # Wait for client connection.
    print('Server started!')
    print('Waiting for clients...')

    while True:
        c, addr = my_socket.accept()              # Establish connection with a client.

        if number_connected_clients == max_number_of_clients:
            c.close()
            print('Refused connection from ' + str(addr) + '. Too many clients.')
            continue

        print('Got connection from ' + str(addr))
        new_thread = Thread(target=on_new_client, args=(c, addr, ser))
        new_thread.setDaemon(True)
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
