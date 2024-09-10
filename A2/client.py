import sys 
import socket
import threading
from _thread import *

HEADER = 64
FORMAT = 'ascii'
DISCONNECT_MESSAGE = '/quit'

def recv_thread(cli_socket):
    while True:
        try: 
            data = cli_socket.recv(1024)
            if data == DISCONNECT_MESSAGE:
                break
            print(f"{data.decode(FORMAT)}")
            print("Reply on the line below (or type /quit to leave the chat):")
        except:
            break
        
def send_thread(message, cli_socket):
    cli_socket.send(message.encode(FORMAT))
    
def main():
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
        host_name = str(sys.argv[1])
    
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try: 
            client.connect((host_name, port))
            print("Successfully connected to the server!")
        except: 
            print("Error connecting to server. Please check port and try again")
            
        start_new_thread(recv_thread, (client,))
        print("Type your first message on the line below (or type /quit to leave the chat):")
        
        while True:
            msg = input()
            start_new_thread(send_thread, (msg, client,))
            
            if msg == DISCONNECT_MESSAGE:
                break
            else: 
                continue
            
        client.close()

if __name__ == "__main__":
    main()