#!/usr/bin/env python

import socket
import dpkt
import argparse
import sys
import time

def make_icmp_socket(ttl, timeout):
     # creates a raw socket with ICMP protocol
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        print("ICMP socket successfully created")
    except s.error as e:
        print("Error creating socket:", e)
        exit(1)
    
    # sets the TTL of the ICMP socket to specified TTL
    s.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    # set the timeout of the ICMP socket
    s.settimeout(timeout)

    try:
        host_ip = socket.gethostbyname("127.0.0.1")
    except socket.gaierror:
        print("Error resolving host")
        sys.exit()
    return s, host_ip

def send_icmp_echo(socket, payload, id, seq, destination):
    echo = dpkt.icmp.ICMP.Echo(id=id, seq=seq, data=payload)
    packet = dpkt.icmp.ICMP(type=dpkt.icmp.ICMP_ECHO, data =echo)
    socket.sendTo(packet, (destination, 1))

def recv_icmp_response():
    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        start = time.time()
        print("ICMP socket successfully created")
    except rs.error as e:
        print("Error creating socket:", e)
        exit(1)
    while True:
        recPacket, addr = rs.recvfrom(1024)
        ICMPHeader = recPacket[20:28]
    return 

def main():
    parser = argparse.ArgumentParser(description ='ICMP server parameters' )
    parser.add_argument('-ttl', type=int, required=True)
    # what do we want default timeout to be?
    parser.add_argument('-timeout', type=int, default=10)
    parser.add_argument('-destination', type=int, default=10, required=True, help="IP address of destination")
    parser.add_argument('-n', type=int, help="Number of packets", required=True)
    args = parser.parse_args()

    payload = "hello"
    new_socket, host_ip = make_icmp_socket(args.ttl, args.timeout)
    for i in range(args.n):
        send_icmp_echo(new_socket, payload, i, i, args.destination)

if __name__ == "__main__":
    main()