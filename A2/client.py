import sys 
import socket
import threading
from _thread import *

FORMAT = 'ascii' # format set as ascii
DISCONNECT_MESSAGE = '/quit' # quit message set to /quit

# function to continuously receive messages from other clients in the chat room
def recv_thread(cli_socket):
    while True:
        try: 
            data = cli_socket.recv(1024)
            if data == DISCONNECT_MESSAGE:
                break
            # message from other clients is decoded and printed
            print(f"{data.decode(FORMAT)}")
            print("Reply on the line below (or type /quit to leave the chat):")
        except:
            break

# function to send an encoded message to a client 
def send_thread(message, cli_socket):
    cli_socket.send(message.encode(FORMAT))
    
def main():
    # checks if command line input is valid
    if len(sys.argv) != 3:
        print("Invalid parameters. Please try again")
    elif len(sys.argv) == 3:
        port = int(sys.argv[2]) # port number
        host_name = str(sys.argv[1]) # host name
    
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # set up the client socket
        
        # attempts to connect the client to the server
        # exits if any errors occur
        try: 
            client.connect((host_name, port))
            print("Successfully connected to the server!")
        except: 
            print("Error connecting to server. Please check port and try again")
        
        # start a new thread for each client socket to continuously receive messages while thread is open
        recvd_thread = threading.Thread(target = recv_thread, args= ((client,)))
        recvd_thread.start()
        
        print("Type your first message on the line below (or type /quit to leave the chat):")
        
        # loop that allows a client to continuously send messages to server with the send_thread function
        while True:
            msg = input()
            sent_thread = threading.Thread(target = send_thread, args= (msg,client,))
            sent_thread.start()
            
            if msg == DISCONNECT_MESSAGE:
                break
            else: 
                continue
            
        client.close() # closes the client connection to server

if __name__ == "__main__":
    main()