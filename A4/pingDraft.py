import threading
import socket
import argparse
import sys
import time
import struct
import dpkt

# Constants
ICMP_ECHO_REQUEST = 8
IP_MAXPACKET = 65535
IP4_HDRLEN = 20  # IPv4 header length
ICMP_HDRLEN = 8  # ICMP header length

# create global variables for ttl and timeout
ttl = 100
ttl = 100

# create default payload data
PAYLOAD_DATA = "CS3640 Assignment 4"

# Store RTTs for calculating average
rtts = []
successful_pings = 0


#might not be the right way to calculate checksum?
def checksum(source_string):
    # calculate a checksum for the header
    csum = 0
    countTo = (len(source_string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal =  ord(str[count+1]) * 256 + ord(str[count])
        csum += thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(source_string):
        csum = csum + ord(str[len(str) - 1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def make_icmp_socket(ttl, timeout):
    # create a raw server with ICMP protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    s.settimeout(timeout)

    try:
        host_ip = socket.gethostbyname("127.0.0.1")
    except socket.gaierror:
        print("Error resolving host")
        sys.exit()
    return s, host_ip

def send_icmp_echo(sock, payload, id, seq, destination):
    # Encode the payload
    payload = payload.encode()
    # Create the ICMP Echo Request
    echo_request = dpkt.icmp.ICMP.Echo(id=id, seq=seq, data=payload)
    # Create the ICMP packet and set its type to ICMP_ECHO
    icmp_packet = dpkt.icmp.ICMP(type=dpkt.icmp.ICMP_ECHO, data=echo_request)
    # Convert the ICMP packet to bytes
    icmp_bytes = bytes(icmp_packet)
    # Send the packet to the destination
    sock.sendto(icmp_bytes, (destination, 1))
    # Record the time of sending for RTT calculation
    start_time = time.time()
    return start_time

def recv_icmp_response(sd, destination, icmp_seq, icmp_id, start_time):
    global rtts, successful_pings
    
    try:
        # Receive packet
        rec_data, addr = sd.recvfrom(IP4_HDRLEN + ICMP_HDRLEN + 64)  # You can specify the length
        
        # Record time and calculate RTT
        end_time = time.time()
        rtt = (end_time - start_time) * 1000  # Convert to ms
        rtts.append(rtt)
        successful_pings += 1

        # Unpack the IP header (first 20 bytes)
        ip_header = struct.unpack('!BBHHHBBH4s4s', rec_data[:IP4_HDRLEN])

        # Source and destination IP addresses
        src_ip = socket.inet_ntoa(ip_header[8])
        dst_ip = socket.inet_ntoa(ip_header[9])

        # Unpack the ICMP header
        icmp_header = struct.unpack('!BBHHH', rec_data[IP4_HDRLEN:IP4_HDRLEN + ICMP_HDRLEN])
        icmp_type = icmp_header[0]

        # TTL (Time-To-Live)5
        ttl = ip_header[5]

        # Print the required information
        print(f"destination = {destination}; icmp_seq = {icmp_seq}; icmp_id = {icmp_id}; ttl = {ttl}; rtt = {rtt:.1f} ms")
        
    except socket.error as err:
        print(f"recvfrom() failed: {err}")

def calc_avg_rtt(rtts, num_pings):
    if rtts:
        avg_rtt = sum(rtts) / len(rtts)
        print(f"Average rtt: {avg_rtt:.1f} ms; {successful_pings}/{num_pings} successful pings.")
    else:
        print(f"0/{num_pings} successful pings.")

def main():
    global ttl, timeout
    #command to run: sudo python3 pingDraft.py -ttl 64 -timeout 1 -destination 8.8.8.8 -n 3
    parser = argparse.ArgumentParser(description='ICMP server parameters')
    parser.add_argument('-ttl', type=int, required=True, help="Time-to-Live for the ICMP packet")
    parser.add_argument('-timeout', type=int, default=100, help="Time-to-Live for the ICMP packet")
    parser.add_argument('-destination', type=str, required=True, help="IP address of the destination")
    parser.add_argument('-n', type=int, required=True, help="Number of packets to send")
    args = parser.parse_args()

    payload = PAYLOAD_DATA
    ttl = args.ttl

    if args.timeout:
        timeout = args.timeout
    
    new_socket, host_ip = make_icmp_socket(args.ttl, args.timeout)

    for i in range(args.n):
        # Record time when sending the packet
        start_time = time.time()
        
        # Send ICMP echo requests
        send_icmp_echo(new_socket, payload, i, i, args.destination)
        
        # Create a new thread to receive ICMP response
        new_thread = threading.Thread(target=recv_icmp_response, args=(new_socket, args.destination, i, i, start_time))
        new_thread.start()
        
        # Wait between sending packets
        time.sleep(1)

    # Wait for all threads to complete before calculating averages
    new_thread.join()

    # Calculate and print average RTT
    calc_avg_rtt(rtts, args.n)

if __name__ == "__main__":
    main()
