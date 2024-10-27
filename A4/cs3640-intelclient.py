import socket
import json
import dnspython

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 5555
valid_Request = False
request_Options = ["IPV4_ADDR", "IPV6_ADDR", "TLS_CERT", "HOSTING_AS", "ORGANIZATION"]

s.connect((host, port))
print (s.recv(1024))

while valid_Request == False:
    # Send a diagnostic request
    request = input("Please choose a diagnostic request (as written): IPV4_ADDR, IPV6_ADDR, TLS_CERT, HOSTING_AS, or ORGANIZATION")
    if request not in request_Options:
        print("Invalid request, please try again.")
        continue
    else:
        valid_Request = True
s.send(json.dumps(request).encode('utf-8'))

# Receive the response
response = s.recv(1024).decode('utf-8')
print("Received response:", json.loads(response))

s.close()

# The client needs to accept the following command-line arguments:
#• intel_server_addr: The address of the Intel Server.
#• intel_server_port: The port on which the Intel Server is listening.
#• domain: The domain to query. 
#• service: The network intelligence service to request (e.g., IPV4_ADDR, IPV6_ADDR, TLS_CERT, HOSTING_AS, ORGANIZATION).