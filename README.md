# PSA-P2-PTU-Project


# Installation

## Python libraries
To install required python libraries, use: 
```
pip install -r requirements.txt
```
To generate a new requirement file, use:
```
pip install pipreqs
pipreqs /path/to/project
``` 


## Other dependencies

    sudo apt-get update
    sudo apt-get install gtkterm
    sudo apt-get install mpg321
    

# RS232 Communication parameters

9600 baud rate (using 38400) 
8 bits data
1 stop bit
1 start bit
no parity

If you want more information about RS232, feel free to watch [this video](https://www.youtube.com/watch?v=AHYNxpqKqwo).

# person_detector
To run `person_detector` follow this steps:

1. run `create_encodings.py` to create encodings of known faces ( known faces are locted in `faces`) and genarate a pickle file `encodings.pickle`
2. run `person_detector`
    - this code will get face encodings form `encodings.pickle`
    - then will open camera and read frame



- opencv have some pre-trained algorithms to identifie faces.
- it's necessary to create a folder (images) where we will store some faces so the programe can compare and identify 
 
 # voice server

- import socket
- import gTTs
- import os
- Defenition of function on_new_client
- Configuration socket communication
- Cycle attending to new client connection requests

# manager client

- import socket
- defenition of function main

# ptu server/client
For server:

    python3 scripts/project_ptu/ptu_server.py

For client:

    python3 scripts/project_ptu/ptu_client.py

    
