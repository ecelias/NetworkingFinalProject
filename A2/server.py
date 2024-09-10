import sys 
import socket
from _thread import *
import threading

## used https://www.geeksforgeeks.org/socket-programming-multi-threading-python/ to learn syntax for multi-threading
## used https://www.geeksforgeeks.org/socket-programming-python/ to learn more about the syntax for socket programming 

file1 = open('/home/ecelias/cs3640/A2/output.txt', 'w+')
file1.write('\n')
file1.write('\n')

def write_to_file(message):
    file1.write(message)
    file1.write('\n')

HEADER = 64
FORMAT = 'ascii'
DISCONNECT_MESSAGE = '/quit'

clients = set()
    
def threaded(connection):
    clients.add(connection)
    while True:
        data = connection.recv(1024)
        recv_msg = f'Message received from {connection}: {data}'
        write_to_file(recv_msg)
        if not data:
            print("Goodbye")
            quit_msg = f'{connection} has disconnected.'
            write_to_file(quit_msg)
            break
        else:
            for client in clients:
                sent_msg = f'Message from {connection} sent: {data}'
                write_to_file(sent_msg)
                client.send(data)
    connection.close()

def main():
    if len(sys.argv) == 2:
        port = sys.argv[1]
    
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        default_port = int(port)
    
        try:
            host_ip = socket.gethostbyname("127.0.0.1")
        except socket.gaierror:
            print("Error resolving host")
            sys.exit()

        tcp.bind((host_ip, default_port))
        print(f'The socket has successfully connected to {default_port}')
    
        tcp.listen(6)
        print(f"Listening on {host_ip}:{default_port}")
    
        while True:
            connection, address = tcp.accept()
            conn_accepted_msg = f'Connection from {address} received.'
            file1.write(conn_accepted_msg)
            print(conn_accepted_msg)

            start_new_thread(threaded, (connection,))
            #print(f'Current active connections: {threading.active_count()}')
            
    tcp.close()
        
if __name__ == "__main__":
    main()
