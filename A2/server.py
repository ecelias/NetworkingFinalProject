import sys 
import socket
from _thread import *
import threading

# opens the output file
file1 = open('output.txt', 'w+')

# writes a message to the output file
def write_to_file(message):
    file1.write(message)
    
write_to_file('ecelias Elizabeth Elias\n')

FORMAT = 'ascii' # format set as ascii
DISCONNECT_MESSAGE = '/quit' # quit message set to /quit

clients = set() # a set to hold all current clients
    
# a function to continuously run threads that handle sending and receiving messages
def threaded(connection):
    clients.add(connection)
    connection_string = connection.getpeername()
    connection_name = connection_string[1]
    
    while True:
        data = connection.recv(1024) 
        data = data.decode(FORMAT)
        recv_msg = f'\nMessage from user [{connection_name}]: {data}'
        # if the program is forcefully executed or the disconnect message is received
        # remove the connection from the set of clients and break the thread
        if not data or data == DISCONNECT_MESSAGE:
            print("Goodbye")
            quit_msg = f'\nUser {connection_name} has left the chat.'
            write_to_file(quit_msg)
            write_to_file(f'\n')
            clients.remove(connection)
            break
        else:
            write_to_file(recv_msg)
            # sends a message to every client in the set of clients except for the current connection
            for client in clients:
                if client != connection:
                    # get peer name returns the username of the client
                    client_name = client.getpeername()[1]
                    sent_msg = f'\nMessage from user [{connection_name}] sent to user [{client_name}]'
                    write_to_file(sent_msg)
                    # sends the ascii-encoded message to each client
                    client.send(recv_msg.encode(FORMAT))
            write_to_file(f'\n')
    connection.close() # closes the connection

def main():
    # checks if command line input is valid
    if len(sys.argv) != 2:
        print("Invalid parameters. Please try again")
    elif len(sys.argv) == 2:
        port = sys.argv[1]
    
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates the TCP socket
    
        default_port = int(port)
    
        try:
            host_ip = socket.gethostbyname("127.0.0.1")
        except socket.gaierror:
            print("Error resolving host")
            sys.exit()

        tcp.bind((host_ip, default_port)) # binds the socket to an address specified by the port
        print(f'The socket has successfully connected to {default_port}')
    
        tcp.listen(6) # listens for any incoming message requests
        print(f"Listening on {host_ip}:{default_port}")
    
        while True:
            # accepts a new connection after socket is bound and listening for connections
            # connection is the new socket used to send and receive data
            # address is the address bound to socket on other end of the connection
            connection, address = tcp.accept()
            conn_accepted_msg = f'\nUser {address[1]} has joined the chat.'
            write_to_file(conn_accepted_msg)
            write_to_file(f'\n')
            print(conn_accepted_msg)
            
            # starts a new thread for every client that attempts to establish a connection
            new_thread = threading.Thread(target = threaded, args= (connection,))
            new_thread.start()
            #print(f'Current active connections: {threading.active_count()}')
            
    tcp.close() # closes the server
        
if __name__ == "__main__":
    main()

# closes the output file
file1.close()