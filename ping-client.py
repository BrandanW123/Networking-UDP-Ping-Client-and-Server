#! /usr/bin/env python3
# Echo Client
import sys
import socket
from timeit import default_timer as timer
from struct import *
from decimal import *


# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
count = int(sys.argv[2])
# Sequence number holder/counter
sequence_num = 1 
# Counts num. of dropped periods
dropped_num = 0
# Number of Pings
num = 10 
#Holds sec values (Min, Max,and Average) times
min_rttime = 0
max_rttime = 0
avg_rttime = 0

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Timeout function w/ 1 sec. parameter after a period of inactivity (use to mess with timeout setting)
clientsocket.settimeout(1)

print("Pinging " + str(port) + ", " + host)

# Unpack and Responds with PING or Time Out ERROR
def response_from(): 
    global dropped_num
    global count
    global sequence_num
    global sequence_num2
    global dataEcho
    while True:
        try:
            packed_data, address = clientsocket.recvfrom(count)
            unpacked_data = unpack('!hH', packed_data)
            sequence_num = unpacked_data[1]
            return "PING"
        except Exception as e:
            dropped_num+=1
            return "Ping message "+ str(sequence_num) + " timed out"


# Sends the packets to server        
def send_message(message, wait = False): # Sends the packets to server
    packed_data = pack('!hH', 1, sequence_num)
    clientsocket.sendto(packed_data,(host, port))

    if wait == False:
        return
    else:
        return response_from()


# Loop controlling Number of Sending & Recieving transmission   
while sequence_num <= num:
    start = timer() # Starting timer
    data = ""
    dataEcho = ""
    recieved = send_message(data, True)
    end = timer() # Ending timer
    recieved_type = recieved # Stores return value
    rrttime = end - start # Calculate sec
    if recieved_type == "PING": # Excute when return value is PING
        print("Ping message number " + str(sequence_num) + " RTT: %f6 sec" % rrttime)
        avg_rttime = avg_rttime + rrttime
        if rrttime < min_rttime or min_rttime == 0:
          min_rttime = rrttime
        if rrttime > max_rttime or max_rttime == 0:
          max_rttime = rrttime

    else: # Excute when return value is Timeout or not PING and prints what was returned
        print(recieved)

    sequence_num+=1 # Increments Sequence

# Closes the client socket
clientsocket.close()

# Calculate Recieved Values & Package Lost Percentage 
recieved = num - dropped_num
percentage = dropped_num * 10

# Prints Statistics after the num of Sending & Recieving Transmission
print("\nStatistics:")
print(str(num) + " packets trasmitted, " + str(recieved) + " recieved, " + str(percentage) + "% packetloss")
print("Min/Max/Avg RTT: min= %f6 / %f6 / %f6" % (min_rttime, max_rttime, (avg_rttime/num)))

      
