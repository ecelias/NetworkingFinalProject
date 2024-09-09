import sys 
import socket
from _thread import *
import threading

## used https://www.geeksforgeeks.org/socket-programming-multi-threading-python/ to learn syntax for multi-threading
## used https://www.geeksforgeeks.org/socket-programming-python/ to learn more about the syntax for socket programming 


def main():
    if len(sys.argv) == 2:
        port = sys.argv[1]
    
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        default_port = int(port)
    
        try:
            host_ip = socket.gethostbyname("127.0.0.1")
            print(host_ip)
        except socket.gaierror:
            print("Error resolving host")
            sys.exit()

        tcp.bind((host_ip, default_port))
        print(f'The socket has successfully connected to {default_port}')
    
        tcp.listen(6)
        print(f"Listening on {host_ip}:{default_port}")
    
        while True:
            connection, address = tcp.accept()
            print(f'Connection from {address} received.')
        
            connection.send("You've connected to the server".encode())
        
            connection.close()
            break
        
if __name__ == "__main__":
    main()
