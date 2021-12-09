import os
import asyncio
import time

#--------------------------------------------------------#
#I opted to go with a high level implementation of network IO using
#the asynchronous library. I wrote the server with async also but changed to
#low level sockets because I couldnt figure out how to get out of the event loop
#from the callback function that processes inputs

#------------------Send Data through Stream Object ---------------------#
async def send_data(message, reader, writer):

    #send_data sends data and recieves data over the "reader" and "writer" Stream objects
    print(f'{time.strftime("%H:%M:%S")} Send: {len(message)}')
    writer.write(message)
    await writer.drain()

    data = await reader.read(1024)
    print(f'Response: {data}')

#------------------------------------------------------------------------#

#--------------- Read data from file and send to server -----------------#
async def read_and_send_data(fd, reader, writer):

    data = fd.read(1024) #read 1024 bytes at a time
    while(data != b''):
        #read file until EOF b''
        returned = await send_data(data, reader, writer)
        #print("returned data: ", returned)
        data = fd.read(1024)
#------------------------------------------------------------------------#

#--------------- Recieve Data from server and Write to File -------------#
async def receive_and_write_data(fd, reader, writer):

    counter = 0
    data = await reader.read(1024)
    while(len(data) == 1024): #infer end of stream by data less than buffer length
        print("Writing data to file: ", len(data), " ", counter)
        fd.write(data)
        counter += 1
        data = await reader.read(1024)
    fd.write(data)
#------------------------------------------------------------------------#

async def main():

    os.system('clear')
    #open a connection to server. use reader and writer streams so recieve/send data
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    #open stl file for transfering over network
    fd = open('cad_mesh.stl', 'rb')
    await read_and_send_data(fd, reader, writer)
    fd.close()
    #close file after reading

    #open file for writing
    fd = open('cad_mesh.csv', 'w+b')
    await receive_and_write_data(fd, reader, writer)
    fd.close()

    #list directory contents
    os.system('ls -l')


os.system('clear')
asyncio.run(main())