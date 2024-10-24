import threading
import socket
import argparse
import sys
import time
import struct
import ctypes

# Constants
ICMP_ECHO_REQUEST = 8
IP_MAXPACKET = 65535
IP4_HDRLEN = 20  # IPv4 header length
ICMP_HDRLEN = 8  # ICMP header length

# Store RTTs for calculating average
rtts = []
successful_pings = 0


#might not be the right way to calculate checksum?
def checksum(source_string):
    """Calculate the checksum of the input string."""
    sum = 0
    countTo = (len(source_string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count = count + 2

    if countTo < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def make_icmp_socket(ttl, timeout):
    """Creates a raw ICMP socket."""
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    s.settimeout(timeout)
    try:
        host_ip = socket.gethostbyname("127.0.0.1")
    except socket.gaierror:
        print("Error resolving host")
        sys.exit()
    return s, host_ip

#problem: code is not using dpkt module
def send_icmp_echo(socket, payload, id, seq, destination):
    """Construct and send an ICMP echo request."""
    payload = payload.encode()
    
    # Build the ICMP Echo Request header
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, 0, id, seq)
    
    # Data to be sent (encoded payload)
    data = struct.pack("d", time.time()) + payload
    
    # Calculate the checksum -- Needs valid checksum to send
    packet = header + data
    chksum = checksum(packet)
    
    # Rebuild the header with the correct checksum
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, chksum, id, seq)
    
    # Final packet (header + data)
    packet = header + data

    # Send the packet to the destination
    socket.sendto(packet, (destination, 1))

def recv_icmp_response(sd, destination, icmp_seq, icmp_id, start_time):
    """Receive and parse the ICMP response, calculate RTT and print details."""
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

        # TTL (Time-To-Live)
        ttl = ip_header[5]

        # Print the required information
        print(f"destination = {destination}; icmp_seq = {icmp_seq}; icmp_id = {icmp_id}; ttl = {ttl}; rtt = {rtt:.1f} ms")
        
    except socket.error as err:
        print(f"recvfrom() failed: {err}")

def main():

    #command to run: python script_name.py -ttl 64 -timeout 1 -destination 8.8.8.8 -n 3

    parser = argparse.ArgumentParser(description='ICMP server parameters')
    parser.add_argument('-ttl', type=int, required=True, help="Time-to-Live for the ICMP packet")
    parser.add_argument('-timeout', type=int, default=1, help="Timeout for the ICMP socket")
    parser.add_argument('-destination', type=str, required=True, help="IP address of the destination")
    parser.add_argument('-n', type=int, required=True, help="Number of packets to send")
    args = parser.parse_args()

    payload = "hello"
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
    if rtts:
        avg_rtt = sum(rtts) / len(rtts)
        print(f"Average rtt: {avg_rtt:.1f} ms; {successful_pings}/{args.n} successful pings.")
    else:
        print(f"0/{args.n} successful pings.")

if __name__ == "__main__":
    main()
