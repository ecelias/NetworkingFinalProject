import socket
import json
import dns.resolver

##credit reel: https://www.geeksforgeeks.org/network-programming-in-python-dns-look-up/ - used for IP address retrieval 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 5555
domain = ""

s.bind((host, port))
s.listen(5)

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        try:
            request = json.loads(data)
            # Process the request and generate diagnostic results
            result = process_diagnostics(request)

            # Send the response back to the client
            response = json.dumps(result)
            client_socket.send(response.encode('utf-8'))

        except Exception as e:
            print("Error processing request:", e)

def process_diagnostics(request):
    # Perform diagnostic analysis based on the received request
    # Each implemented as a single request

    def IPV4_ADDR(domain):
        try:
            # Use DNS resolver to get the IPv4 address of the domain
            v4_Address_Success = dns.resolver.resolve(domain, 'A')
            return v4_Address_Success
        except:
            return "Error: Unable to resolve domain"
    if request == IPV4_ADDR:
        IPV4_ADDR(domain)
    
    def IPV6_ADDR(domain):
        try:
            # Use DNS resolver to get the IPv6 address of the domain
            v6_Address_Success = dns.resolver.resolve(domain, 'AAAA')
            return v6_Address_Success
        except:
            return "Error: Unable to resolve domain"
    if request == IPV6_ADDR:
        IPV6_ADDR(domain)
    
    def TLS_CERT(domain):
        #return the TLS/SSL certificate associated with the queried domain or return an error message ("certificate cannot be retrieved" or similar)
        #use python's ssl module to retrieve certificate
        return
    if request == TLS_CERT:
        TLS_CERT(domain)
    
    def HOSTING_AS(domain): 
        #The server should return the Autonomous System (AS) that
        #hosts the queried domain’s IP. You must first resolve the IP address associated with the
        #domain and then use a WHOIS service to obtain the AS information. If the AS cannot be
        #determined, the server must return an appropriate error message.
        return
    if request == HOSTING_AS:
        HOSTING_AS(domain)
    
    def ORGANIZATION(domain): 
        #The server should return the name of the organization
        #associated with the domain’s TLS certificate. You must parse the subject’s Organization
        #Name from the certificate. If the organization cannot be determined, the server must return
        #an appropriate error message.
        return
    if request == ORGANIZATION:
        ORGANIZATION(domain)
    
    return {"status": "success", "message": "Diagnostics completed"}

    
def main ():
    while True:
        print("Server listening on " + str(host))
        c, addr = s.accept()
        print("Connected to %s" % str(addr))
        c.send("Hello socket")

        handle_client(c)
        c.close()

if __name__ == "__main__":
    main()
    



