import sys 
import socket

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
    
    tcp.listen(0)
    print(f"Listening on {host_ip}:{default_port}")
    
    while True:
        cli, address = tcp.accept()
        print(f'Connection from {address} received.')
        
        cli.send("You've connected to the server".encode())
        
        cli.close()
        break
    