import socket
import json
import dns.resolver
import ssl
from ipwhois import IPWhois
import OpenSSL
import threading
from datetime import datetime
import os

ORG_PORT = 443
s = ""

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
    client_socket.close()

def get_certificate(host, port=443):
    context = ssl.create_default_context()
    conn = socket.create_connection((host, port))
    sock = context.wrap_socket(conn, server_hostname=host)
    der_cert = sock.getpeercert(True)
    return ssl.DER_cert_to_PEM_cert(der_cert)

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
        # ##### Prints full cert to server
        # # Create a raw socket and connect to the server
        # raw_socket = socket.create_connection((domain, 443))
        
        # # Create an SSL context and configure it for hostname verification
        # sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        # sslContext.check_hostname = True
        # sslContext.verify_mode = ssl.CERT_REQUIRED
        
        # # Wrap the raw socket with SSL and get the certificate
        # wrapped_socket = sslContext.wrap_socket(raw_socket, server_hostname=domain)
        # cert = wrapped_socket.getpeercert()
        
        # # Close the SSL socket after retrieving the certificate
        # wrapped_socket.close()
        # print (cert)
        # ######

        ###### returns parsed parts to client
        certificate = get_certificate(domain)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)

        sub = dict(x509.get_subject().get_components())
        comp = dict(x509.get_issuer().get_components())
        ver = x509.get_version()
        ser = x509.get_serial_number()

        decode_subjects = {}
        decode_components = {}

        for key in sub.keys():
            current_key = key.decode('utf-8')
            current_value = sub.get(key)
            decode_subjects[current_key] = current_value.decode('utf-8')

        for key in comp.keys():
            current_key = key.decode('utf-8')
            current_value = comp.get(key)
            decode_components[current_key] = current_value.decode('utf-8')


        decoded_results = {
            'subject': decode_subjects,
            'issuer': decode_components,
            'version': str(ver),
            'serial_number': str(ser),
        }
        return decoded_results
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
        certificate = get_certificate(domain)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)
        components = dict(x509.get_issuer().get_components())

        for key in components.keys():
            current_key = key.decode('utf-8')
            current_value = components.get(key)
            if current_key == 'O':
                return current_value.decode('utf-8')

        return "Error: Organization information unavailable in certifacte"
    except Exception as e:
        return f"Error: Unable to obtain organization information: {e}"

def process_diagnostics(request):
    # Perform diagnostic analysis based on the received request

    # extract domain and service requested from json file
    domain = request.get("domain")
    service = request.get("service")

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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 5555
    s.bind((host, port))
    s.listen(5)
    print("Server listening on " + str(host))

    while True:
        c, addr = s.accept()
        print("Connected to %s" % str(addr))
        handle_client(c)
        c.close()


        # new_thread = threading.Thread(target = handle_client, args= (c,))
        # new_thread.start()

if __name__ == "__main__":
    main()
