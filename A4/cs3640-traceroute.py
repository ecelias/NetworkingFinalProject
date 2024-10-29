#!/usr/bin/env python
import threading, socket, argparse, sys, time, struct
import dpkt

ICMP_ECHO_REQUEST = 8
DISCONNECT_MESSAGE = "time limit reached"
PAYLOAD_DATA = "CS3640 Assignment 4"
ttl = 1
timeout = 100

def make_icmp_socket(ttl, timeout):
     # creates a raw socket with ICMP protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    # sets the TTL of the ICMP socket to specified TTL
    s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    # set the timeout of the ICMP socket
    s.settimeout(timeout)
    return s

def send_icmp_echo(socket, id, seq, destination):
    #payload = payload.encode()
    echo = dpkt.icmp.ICMP.Echo(id=id, seq=seq, data=b'')
    # packet = dpkt.icmp.ICMP(type=dpkt.icmp.ICMP_ECHO, data=echo)
    packet = dpkt.icmp.ICMP(type = dpkt.icmp.ICMP_ECHO, data = echo)
    socket.sendto(bytes(packet), (destination, 0))

def get_hop_ip(s, destination, ttl, timeout):
    send_icmp_echo(s, 1, ttl, destination)
    try:
        msg, addr = s.recvfrom(1024)
        return addr[0]
    except socket.timeout:
        return None
        
def get_route(ttl, timeout, payload, ip, seq, destination, current_hop):
    try: 
        with make_icmp_socket(ttl, timeout) as tr_socket:

        #tr_socket = make_icmp_socket(ttl, timeout)
            start = time.time()
            addr = get_hop_ip(tr_socket, destination, ttl, timeout)

            end = time.time()
            rtt = round((end - start) * 1000, 1)
            print(f"destination = {destination}; hop {current_hop} = {addr}; rtt = {rtt} ms")
            return rtt
    except socket.timeout:
        print (f"destination = {destination}; hop {hop} = *; ttl = {ttl}; request timed out.")
    except Exception as e:
        print (f'An error has occured: {e}')
    # if str(msg) == str(destination):
    #     return

def main():
    global ttl, timeout, hop
    parser = argparse.ArgumentParser(description ='ICMP server parameters' )
    parser.add_argument('-timeout', type=int, default = 100)
    parser.add_argument('-destination', required=True, help="IP address of destination")
    parser.add_argument('-n_hops', type=int, help="Max hops", required=True)
    parser.add_argument('-ttl', type=int)
    
    # parse command line arguments for the program
    args = parser.parse_args()
    if args.ttl:
        ttl = args.ttl
    if args.timeout:
        timeout = args.timeout

    payload = PAYLOAD_DATA
    
    for hop in range(1, args.n_hops+1):
        rtt = get_route(ttl,timeout, payload, ttl, ttl,args.destination, hop)
        ttl+=1
        if rtt is None:
            print (f'Failed to retrieved hop {hop}')
            break

    # if args.n_hops == 0:
    #     print("Zero hops indicated")
    # elif args.n_hops > 0:
    #     for hop in range(1, args.n_hops + 1):
    #         get_route(ttl, timeout, payload, hop, hop, args.destination, hop)
            

if __name__ == "__main__":
    main()
                