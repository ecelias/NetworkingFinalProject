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

    socket.sendto(packet, (destination, 1))

# def recv_icmp_response():
#     rs = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
#     rs.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
    
#     while True:
#         recPacket, addr = rs.recvfrom(1024)
#         ICMPheader = recPacket[20:28]
#         if not recPacket:
#             break
#         else:
#             print(recPacket.decode())
#             type, code, checksum, p_id, sequence = struct.unpack('bbHHh', ICMPheader)
#             print(f"type: [{str(type)}] code: [{ + str(code)}] checksum: [{ str(checksum)}] p_id: [{str(p_id)}] sequence: [{str(sequence)}]")
#             rs.close()
#     # #deadline = time.time()
#     # print("ICMP socket successfully created")
#     # recPacket, addr = rs.recvfrom(1024)
#     # print(recPacket.decode())
#     # ICMPheader = recPacket[20:28]
#     # type, code, checksum, p_id, sequence = struct.unpack('bbHHh', ICMPheader)
#     # print(f"type: [{str(type)}] code: [{ + str(code)}] checksum: [{ str(checksum)}] p_id: [{str(p_id)}] sequence: [{str(sequence)}]")
#     rs.close()

def recv_icmp_response():
    rs = make_icmp_socket(ttl, timeout)
    msg = rs.recv(1024)
    return msg

def avg_rtt(count, trips):
    avg_time = 0
    num_trips = 0
    for trip in trips:
        avg_time += trip
        num_trips +=1
    avg_time = round((avg_time/len(trips)), 1)
    print("Average rtt: " + str(avg_time) + " ms; " + str(count) + "/" + str(len(trips)) + " successful " "pings.")


def do_ping(num_pings, dest):
    # create variables to hold the rtt from the pings and number of trips
    trips = []
    successful_trips = 0

    # set a string as the payload (??? should this be something else)
    payload = PAYLOAD_DATA

    # create an ICMP socket 
    new_socket = make_icmp_socket(ttl, timeout)
    for i in range(num_pings):
        start = time.time()
        try: 
            send_icmp_echo(new_socket, payload, i, i, dest)
            db = recv_icmp_response()
            successful_trips += 1
        except TimeoutError:
            successful_trips +=0
        end = time.time()
        rtt = round((end - start) * 1000, 1)
        trips.append(rtt)
        print("destination = " + str(dest) + "; icmp_seq = " + str(i) + "; icmp_id = " + str(i),
              "; ttl = " + str(ttl) + "; rtt = " + str(rtt) + " ms")
    avg_rtt(successful_trips, trips)
    print(trips)
    new_socket.close()


def main():
    global ttl, timeout
    parser = argparse.ArgumentParser(description ='ICMP server parameters' )
    parser.add_argument('-ttl', type=int, required=True)
    # what do we want default timeout to be?
    parser.add_argument('-timeout', type=int)
    parser.add_argument('-destination', default=10, required=True, help="IP address of destination")
    parser.add_argument('-n', type=int, help="Number of packets", required=True)
    
    # parse command line arguments for the program
    args = parser.parse_args()
    ttl = args.ttl
    if args.timeout:
        timeout = args.timeout

    do_ping(args.n, args.destination)

if __name__ == "__main__":
    main()