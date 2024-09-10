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
            print(f"Received from server: {data.decode(FORMAT)}")
        except:
            break
        
def send_thread(message, cli_socket):
    cli_socket.send(message.encode(FORMAT))
    
def main():
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
        host_name = str(sys.argv[1])
    
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        client.connect((host_name, port))
        
        start_new_thread(recv_thread, (client,))
        
        while True:
            msg = input("Input message: ")
            start_new_thread(send_thread, (msg, client,))
            
            if msg == DISCONNECT_MESSAGE:
                break
            else: 
                continue
            
        client.close()

if __name__ == "__main__":
    main()