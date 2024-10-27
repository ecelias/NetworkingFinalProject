#!/usr/bin/env python
import threading, socket, argparse, sys, time, struct
import dpkt

ICMP_ECHO_REQUEST = 8
DISCONNECT_MESSAGE = "time limit reached"
PAYLOAD_DATA = "CS3640 Assignment 4"
ttl = 1
timeout = 10

def make_icmp_socket(ttl, timeout):
     # creates a raw socket with ICMP protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    # sets the TTL of the ICMP socket to specified TTL
    s.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    # set the timeout of the ICMP socket
    s.settimeout(timeout)
    return s

def send_icmp_echo(socket, payload, id, seq, destination):
    payload = payload.encode()
    echo = dpkt.icmp.ICMP.Echo(id=id, seq=seq, data=payload)
    # packet = dpkt.icmp.ICMP(type=dpkt.icmp.ICMP_ECHO, data=echo)
    packet = dpkt.icmp.ICMP.Echo()
    packet.type = dpkt.icmp.ICMP_ECHO
    packet.data = echo

    # Make a dummy header with a 0 checksum (??? do we even need this)
    myChecksum = 0
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, id, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    #myChecksum = mychecksum(header + data)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, id, 1)
    packet = header + data

    socket.sendto(bytes(packet), (destination, 1))


def recv_icmp_response():
    rs = make_icmp_socket(ttl, timeout)
    msg = rs.recv(1024)
    return msg


def get_route(ttl, timeout, payload, id, seq, destination, current_hop):
    tr_socket = make_icmp_socket(ttl, timeout)
    start = time.time()
    send_icmp_echo(tr_socket, payload, id, seq, destination)
    msg = recv_icmp_response()

    icmp_header = msg[20:28]
    header = struct.unpack('!BBHHH', icmp_header)
    print(header)

    end = time.time()
    rtt = round((end - start) * 1000, 1)
    print("destination = " + str(destination) + "; hop " + str(current_hop) + " = " + str(header) + "; rtt = " + str(rtt) + " ms")
    if str(msg) == str(destination):
        return
    try: 
        recv_packet, addr = tr_socket.recvfrom(1024)
        rtt = (time.time() - struct.unpack("d", recv_packet[28:36])[0]) * 1000
        print(f"TTL={ttl}, Address={addr[0]}, RTT={rtt:.2f} ms")
    except socket.timeout:
        print("timed out")
    finally:
            tr_socket.close()

def main():
    global ttl, timeout, hop
    parser = argparse.ArgumentParser(description ='ICMP server parameters' )
    parser.add_argument('-timeout', type=int, default=1)
    parser.add_argument('-destination', default=10, required=True, help="IP address of destination")
    parser.add_argument('-n_hops', type=int, help="Max hops", required=True)
    parser.add_argument('-ttl', type=int)
    
    # parse command line arguments for the program
    args = parser.parse_args()
    if args.ttl:
        ttl = args.ttl
    if args.timeout:
        timeout = args.timeout

    payload = PAYLOAD_DATA

    if args.n_hops == 0:
        print("Zero hops indicated")
    elif args.n_hops > 0:
        for hop in range(1, args.n_hops + 1):
            get_route(hop, timeout, payload, hop, hop, args.destination, hop)

if __name__ == "__main__":
    main()
                