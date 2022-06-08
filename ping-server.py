#Brandan Williams
#bcw9
#CS356-010

#! /usr/bin/env python3
# Echo Server
import sys
import socket
import random
from struct import *

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])



# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
sequence_num = 0 # Variable holder

print("The server is ready to receive on port: %s\n" % serverPort)
# Loop forever listening for incoming UDP messages
while True:

    #Generate random numbers Range (0 to 10) pertains to lost packets
    rand = random.randint(0, 10)
    
    # Receive and print the client data from packet socket
    packed_data, address = serverSocket.recvfrom(1024)
    unpacket_data = unpack('!hH', packed_data)
 
    # If statement is true (random # < 4), pakect dropped & don't respond and print dropped message
    if rand < 4:
        print("Message with sequence number %d dropped" % unpacket_data[1])
        continue
        
    # Server will respond & print when random > 4
    print("Responding to ping request with sequence number %d" % unpacket_data[1])
    
    sequence_num = unpacket_data[1]
    packed_data = pack('!hH', 2, sequence_num)  # Packet Sequence and value
    serverSocket.sendto(packed_data,address)    # Sends back value to client

