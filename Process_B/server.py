#server.py
import socket
import os
import numpy as np
from stl import mesh

os.system('clear')

BUF_SIZE = 1024

#---------------BEGIN: Create socket object, bind to localhost anad listen for incoming connections ----------#
#create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#get local machine name
host = socket.gethostname()
port = 8888
#bind to port
server_socket.bind(('127.0.0.1', port))
#listen for up to 5 connections
server_socket.listen(5)
#--------------------END: Create socket object, bind to localhost anad listen for incoming connections ----------#

#--------------------Open file for writing in binary mode. Write incoming data to file.----------#
#open file for writing
fd = open("output", "w+b")
#recieve data in chunks and write to file
client_socket, client_address = server_socket.accept()
while True:
    data = client_socket.recv(BUF_SIZE)
    print("Connection from ", str(client_address), "data: ", len(data))
    fd.write(data)
    client_socket.send(data)
    if(len(data) < BUF_SIZE):
        fd.flush()
        break
        fd.close()
#--------------------------------------------------------------------------------------------------------#

#-------Convert tranfered data file into numpy array and save as CSV------------------------------------- #
#open output file and convert from stl to a Mesh object which contains ndarrays of points
your_mesh = mesh.Mesh.from_file('output')
#extract vertex coordinates to 4 decimal places from Mesh.points (a numpy array) 
X = np.around(your_mesh.points, decimals=4)
#save the rounded points as a CSV file
np.savetxt("output.csv", X, delimiter=',')
#--------------------------------------------------------------------------------------------------------#

#--------------- Open converted csv file as binary and send to client ---------------------------------#
fd = open('output.csv', 'rb')
data = fd.read(1024)
while(data != b''):
    print('sending ', len(data))
    client_socket.send(data)
    data = fd.read(1024)
#--------------------------------------------------------------------------------------------------------#

os.system('ls -l')