import sys 
import socket

if len(sys.argv) == 3:
    port = int(sys.argv[2])
    host_name = str(sys.argv[1])
    print(host_name)
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_ip = "127.0.0.1"
    server_port = 5000
    
    client.connect((host_name, port))
    
    print(client.recv(5000).decode())
    
    client.close()