import socket
import json
import argparse

HOST = '127.0.0.1'
PORT = 5555

def send_request(server_addr, server_port, domain, service):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_addr, server_port))
    #print(s.recv(4096).decode('utf-8'))
    
    # create a dictionary containing the domain queried and service requested
    # this will be sent to the server as a json file
    request_payload = {
        "domain": domain, 
        "service": service
    }
    s.sendall(json.dumps(request_payload).encode('utf-8'))

    # Receive the response
    response = s.recv(4096).decode('utf-8')
    try:
        response_json = json.loads(response)
        print("Received response:", response_json)
    except json.JSONDecodeError:
        print("Error: Invalid response received from server.")

    s.close()

# The client needs to accept the following command-line arguments:
#• intel_server_addr: The address of the Intel Server.
#• intel_server_port: The port on which the Intel Server is listening.
#• domain: The domain to query. 
#• service: The network intelligence service to request (e.g., IPV4_ADDR, IPV6_ADDR, TLS_CERT, HOSTING_AS, ORGANIZATION).


def main():
    parser = argparse.ArgumentParser(description ='ICMP client query server parameters' )
    parser.add_argument('-intel_server_addr', default=HOST, help="Address of intel server")
    parser.add_argument('-intel_server_port', type=int, default=PORT, help="Which port intel server is listening on")
    parser.add_argument('-domain', required=True, help="Domain to query")
    parser.add_argument('-service', required=True, help="Network intelligence service to request")
    
    # parse command line arguments for the program
    args = parser.parse_args()
    #print(f"Arguments received - Server Address: {args.intel_server_addr}, Port: {args.intel_server_port}, Domain: {args.domain}, Service: {args.service}")
   

    request_Options = ["IPV4_ADDR", "IPV6_ADDR", "TLS_CERT", "HOSTING_AS", "ORGANIZATION"]

     # make sure the service requested is valid
    request = args.service
    if request not in request_Options:
        print("Invalid request, please try again.")
        return
    
    # send the request to the server
    send_request(args.intel_server_addr, args.intel_server_port, args.domain, request)



if __name__ == "__main__":
    main()