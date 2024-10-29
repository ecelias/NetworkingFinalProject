import socket
import json
import dns.resolver
import ssl
import urllib.request
from ipwhois import IPWhois

##credit reel: https://www.geeksforgeeks.org/network-programming-in-python-dns-look-up/ - used for IP address retrieval 
##credit reel: https://thelinuxforum.com/articles/180-python-ssl-example - used for TSL/SSL certificate retrieval
##credit reel: https://stackoverflow.com/questions/28997623/how-to-parse-text-in-python-with-ipwhois - used for finding information about AS

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

def IPV4_ADDR(domain):
    try:
        # Use DNS resolver to get the IPv4 address of the domain
        v4_Address_Success = dns.resolver.resolve(domain, 'A')
        return str(v4_Address_Success[0])
    except:
        return "Error: Unable to resolve domain"

def IPV6_ADDR(domain):
    try:
        # Use DNS resolver to get the IPv6 address of the domain
        v6_Address_Success = dns.resolver.resolve(domain, 'AAAA')
        return str(v6_Address_Success[0])
    except:
        return "Error: Unable to resolve domain"
    
def TLS_CERT(domain):
    try: 
        parsed_url = urllib.parse.urlparse(str(domain))
        return (ssl.get_server_certificate((parsed_url.hostname, 443)))
    except: 
        return "Error: Unable to retrieve certificate"
    
def HOSTING_AS(domain): 
    #The server should return the Autonomous System (AS) that
    #hosts the queried domain’s IP. You must first resolve the IP address associated with the
    #domain and then use a WHOIS service to obtain the AS information. If the AS cannot be
    #determined, the server must return an appropriate error message.
    try:
        # Resolve the IP address associated with the domain
        ipv4_records = dns.resolver.resolve(domain, 'A')
        ip_address = str(ipv4_records[0]) 

        # Get the AS information using IPWhois
        obj = IPWhois(ip_address)
        result = obj.lookup_rdap()
        return result['asn']
    except:
        return "Error: Unable to obtain AS information"
    
def ORGANIZATION(domain): 
    #The server should return the name of the organization
    #associated with the domain’s TLS certificate. You must parse the subject’s Organization
    #Name from the certificate. If the organization cannot be determined, the server must return
    #an appropriate error message.
    try:
        return
    except:
        return "Error: Unable to obtain organization information"

def process_diagnostics(request):
    # Perform diagnostic analysis based on the received request

    # extract domain and service requested from json file
    domain = request.domain
    service = request.service

    # Each implemented as a single request
    if service == "IPV4_ADDR":
        return {"result" : IPV4_ADDR(domain)}
    elif service == "IPV6_ADDR":
        return IPV6_ADDR(domain)
    elif service == "TLS_CERT":
        return {"result" : TLS_CERT(domain)}
    elif service == "HOSTING_AS":
        return {"result" : HOSTING_AS(domain)}
    elif service == "ORGANIZATION":
        return {"result" : ORGANIZATION(domain)}
    else:
        return {"error": "Invalid service requested"}
    
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
    



