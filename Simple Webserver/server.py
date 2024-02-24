#import statements
from socket import *
import sys

#server socket setup
serverSocket = socket(AF_INET, SOCK_STREAM)

#Fill in start
serverSocket.bind(('', 10000))
serverSocket.listen(1)
#Fill in end

# main server loop: enters an infinite loop, printing "RTS" and waiting for connection
# As client comes, 'accept()' returns 'connectionSocket' which is for connection and a tuple
while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()  #Fill in start #Fill in end

    try:
        #handling request: these four lines read the HTTP request from the client, give it to the requested filename
        #open that file, and read the contents to 'outputdata'
        message = connectionSocket.recv(1024).decode()  #Fill in start #Fill in end
        filename = message.split()[1]
        f = open(filename[1:])  # Assuming the request is in the format GET /HelloWorld.html HTTP/1.1
        outputdata = f.read()  #Fill in start #Fill in end

        # Sending the response 
        #Fill in start
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode()) #if the file is found, the server sends "200 OK" HTTP
        #code after the contents of file
        #Fill in end
        for i in range(0, len(outputdata)): # Send the content of the requested file to the client
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    # Exception for file not found
    except IOError:
        #send "404 Not Found" message after a HTML error document
        #Fill in start
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>".encode())
        #Fill in end

        #the connetion to the client closed
        #Fill in start
        connectionSocket.close()
        #Fill in end

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
