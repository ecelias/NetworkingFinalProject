import sys 
import socket
from _thread import *
import threading

## used https://www.geeksforgeeks.org/socket-programming-multi-threading-python/ to learn syntax for multi-threading
## used https://www.geeksforgeeks.org/socket-programming-python/ to learn more about the syntax for socket programming 

file1 = open('output.txt', 'w+')
file1.write('ecelias Elizabeth Elias')
file1.write('\n')

def write_to_file(message):
    file1.write(message)

HEADER = 64
FORMAT = 'ascii'
DISCONNECT_MESSAGE = '/quit'

clients = set()
    
def threaded(connection):
    clients.add(connection)
    connection_string = connection.getpeername()
    connection_name = connection_string[1]
    
    while True:
        data = connection.recv(1024)
        data = data.decode(FORMAT)
        recv_msg = f'\nMessage from user [{connection_name}]: {data}'
        if not data:
            print("Goodbye")
            quit_msg = f'\nUser {connection_name} has left the chat.'
            write_to_file(quit_msg)
            write_to_file(f'\n')
            clients.remove(connection)
            break
        else:
            write_to_file(recv_msg)
            for client in clients:
                if client != connection:
                    client_name = client.getpeername()[1]
                    sent_msg = f'\nMessage from user [{connection_name}] sent to user [{client_name}]'
                    write_to_file(sent_msg)
                    #client.send(data.encode(FORMAT))
                    client.send(recv_msg.encode(FORMAT))
            write_to_file(f'\n')
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
            conn_accepted_msg = f'\nUser {address[1]} has joined the chat.'
            write_to_file(conn_accepted_msg)
            write_to_file(f'\n')
            print(conn_accepted_msg)
            start_new_thread(threaded, (connection,))
            #print(f'Current active connections: {threading.active_count()}')
            
    tcp.close()
        
if __name__ == "__main__":
    main()
