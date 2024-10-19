#!/usr/bin/env python
import threading, socket, argparse, sys, time, struct
import dpkt

ICMP_ECHO_REQUEST = 8
DISCONNECT_MESSAGE = "time limit reached"

def make_icmp_socket(ttl, timeout):
     # creates a raw socket with ICMP protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    
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
    payload = payload.encode()
    echo = dpkt.icmp.ICMP.Echo(id=id, seq=seq, data=payload)
    print(echo)
    packet = dpkt.icmp.ICMP(type=dpkt.icmp.ICMP_ECHO, data=echo)

    # Make a dummy header with a 0 checksum
    myChecksum = 0
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, id, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    #myChecksum = mychecksum(header + data)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, id, 1)
    packet = header + data

    socket.sendto(packet, (destination, 1))

def recv_icmp_response():
    rs = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    rs.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
    
    while True:
        recPacket, addr = rs.recvfrom(1024)
        ICMPheader = recPacket[20:28]
        if not recPacket:
            break
        else:
            print(recPacket.decode())
            type, code, checksum, p_id, sequence = struct.unpack('bbHHh', ICMPheader)
            print(f"type: [{str(type)}] code: [{ + str(code)}] checksum: [{ str(checksum)}] p_id: [{str(p_id)}] sequence: [{str(sequence)}]")
            rs.close()
    # #deadline = time.time()
    # print("ICMP socket successfully created")
    # recPacket, addr = rs.recvfrom(1024)
    # print(recPacket.decode())
    # ICMPheader = recPacket[20:28]
    # type, code, checksum, p_id, sequence = struct.unpack('bbHHh', ICMPheader)
    # print(f"type: [{str(type)}] code: [{ + str(code)}] checksum: [{ str(checksum)}] p_id: [{str(p_id)}] sequence: [{str(sequence)}]")
    rs.close()

def main():
    parser = argparse.ArgumentParser(description ='ICMP server parameters' )
    parser.add_argument('-ttl', type=int, required=True)
    # what do we want default timeout to be?
    parser.add_argument('-timeout', type=int, default=1)
    parser.add_argument('-destination', default=10, required=True, help="IP address of destination")
    parser.add_argument('-n', type=int, help="Number of packets", required=True)
    args = parser.parse_args()

    payload = "hello"
    new_socket, host_ip = make_icmp_socket(args.ttl, args.timeout)
    for i in range(args.n):
        send_icmp_echo(new_socket, payload, i, i, args.destination)
        new_thread = threading.Thread(target = recv_icmp_response, args=())
        new_thread.start()
        #recv_icmp_response()

if __name__ == "__main__":
    main()