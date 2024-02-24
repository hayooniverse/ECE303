## To handle multiple HTTP requests simultaneously using threading,'threading' module in Python used 
## In the main loop, the main difference to the single one is here focusing on accepting multiple 
## Connections and dividing them to worker threads rather than processing the requests

from socket import *
import threading

# Function to handle each client request in a separate thread
def handle_client(connectionSocket):
    try:
        # Receive the client's request message
        message = connectionSocket.recv(1024).decode()
        
        # Extract the filename from the received message
        filename = message.split()[1]
        
        # Attempt to open and read the requested file
        with open(filename[1:], 'r') as f:
            outputdata = f.read()

        # Send HTTP response header line to client
        connectionSocket.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n".encode())
        
        # Send the content of the requested file to the client
        connectionSocket.send(outputdata.encode())
        connectionSocket.send("\r\n".encode())
    except IOError:
        # Handle file not found error by sending HTTP 404 response
        connectionSocket.send("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
    finally:
        # Close the client socket
        connectionSocket.close()

# Main function to set up the server
def start_server():
    # Define the server port
    serverPort = 12000
    # Create the server socket (TCP socket)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    
    # Bind the server socket to the specified port
    serverSocket.bind(('', serverPort))
    
    # Start listening for incoming connection requests
    serverSocket.listen(5)
    print(f'The server is ready to receive on port {serverPort}')

    while True:
        # Print message indicating the server is ready to accept a new connection
        print('Ready to serve...')
        
        # Accept an incoming connection request
        connectionSocket, addr = serverSocket.accept()
        
        # Create a new thread to handle the client request
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
        client_thread.start()

# Check if the script is the main program and run the server
if __name__ == "__main__":
    start_server()