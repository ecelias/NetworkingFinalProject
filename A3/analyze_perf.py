import subprocess
import json
import matplotlib.pyplot as plt

def main():
    # Define the bottleneck bandwidths in Mbps - bw other should default to 100? right? i set it in the command anyway lol
    bottleneck_bandwidths = [8, 32, 64]
    # Lists to store results
    tcp_throughput = []
    udp_throughput = []

    # Run network_bottleneck.py for each bandwidth

    for each in bottleneck_bandwidths:
        print(f"Running network_bottleneck.py with {each} Mbps...")
        # ensure that the Mininet's network is clear and prevent errrors in creation and configuration of a new network
        subprocess.call(["sudo", "mn","-c"])
        # call the network bottleneck function
        result = subprocess.call(["sudo", "python3", "network_bottleneck.py", "-bw_other", "100", "-bw_bottleneck", str(each)])
        # Assuming network_bottleneck.py returns throughput in the following format ->
        ## From the JSON files:
        ## "udp_bottleneck_bw": 10,
        ## "udp_other_bw": 100,
        ##
        ## "tcp_bottleneck_bw": 10,
        ## "tcp_other_bw": 100,

    # read all of the json files created by the call to network_bottleneck.py
    # into respective dictionaries
    with open('output-tcp-8-100.json', 'r') as file:
        tcp_test_8 = json.load(file)
    file.close()

    with open('output-tcp-32-100.json', 'r') as file:
        tcp_test_32 = json.load(file)
    file.close()

    with open('output-tcp-64-100.json', 'r') as file:
        tcp_test_64 = json.load(file)
    file.close()

    with open('output-udp-8-100.json', 'r') as file:
        udp_test_8 = json.load(file)
    file.close()

    with open('output-udp-32-100.json', 'r') as file:
        udp_test_32 = json.load(file)
    file.close()

    with open('output-udp-64-100.json', 'r') as file:
        udp_test_64 = json.load(file)
    file.close()

    # calculate the throughput for all the bytes sent and recieved with each type of network
    # tcp_8_throughput = int(tcp_test_8.get("tcp_bytes_received"))/int(tcp_test_8.get("tcp_bytes_sent"))
    # tcp_32_throughput = int(tcp_test_32.get("tcp_bytes_received"))/int(tcp_test_32.get("tcp_bytes_sent"))
    # tcp_64_throughput = int(tcp_test_64.get("tcp_bytes_received"))/int(tcp_test_64.get("tcp_bytes_sent"))

    # udp_8_throughput = int(udp_test_8.get("udp_bytes_received"))/int(udp_test_8.get("udp_bytes_sent"))
    # udp_32_throughput = int(udp_test_32.get("udp_bytes_received"))/int(udp_test_32.get("udp_bytes_sent"))
    # udp_64_throughput = int(udp_test_64.get("udp_bytes_received"))/int(udp_test_64.get("udp_bytes_sent"))

    # calculate the throughput for each test and bottleneck bandwitdth
    # as bytes_recieved/test duration
    
    tcp_8_throughput = int(tcp_test_8.get("tcp_bytes_received"))/int(tcp_test_8.get("tcp_seconds"))
    tcp_32_throughput = int(tcp_test_32.get("tcp_bytes_received"))/int(tcp_test_32.get("tcp_seconds"))
    tcp_64_throughput = int(tcp_test_64.get("tcp_bytes_received"))/int(tcp_test_64.get("tcp_seconds"))

    udp_8_throughput = int(udp_test_8.get("udp_bytes_transmitted"))/int(udp_test_8.get("udp_seconds"))
    udp_32_throughput = int(udp_test_32.get("udp_bytes_transmitted"))/int(udp_test_32.get("udp_seconds"))
    udp_64_throughput = int(udp_test_64.get("udp_bytes_transmitted"))/int(udp_test_64.get("udp_seconds"))
    
    # add the tcp throughput values for all 3 tests to a dictionary
    tcp_throughput.append(tcp_8_throughput)
    tcp_throughput.append(tcp_32_throughput)
    tcp_throughput.append(tcp_64_throughput)

    # add the udp throughput values for all 3 tests fo a dictionary
    udp_throughput.append(udp_8_throughput)
    udp_throughput.append(udp_32_throughput)
    udp_throughput.append(udp_64_throughput)

    # Create the plot
    plt.figure(figsize=(5, 4))
    plt.plot(bottleneck_bandwidths, tcp_throughput, marker='o', label='TCP Throughput (Bps)')
    plt.plot(bottleneck_bandwidths, udp_throughput, marker='o', label='UDP Throughput (Bps)')
    plt.title('Measured Throughput vs Bottleneck Bandwidth')
    plt.xlabel('Bottleneck Bandwidth Set (Mbps)')
    plt.ylabel('Measured Throughput (Bps)')
    plt.xticks(bottleneck_bandwidths)
    plt.legend(['TCP', 'UDP'], loc='upper left')
    
    # Save the plot to analysis.png
    plt.savefig('analysis.png')
    print("Plot saved as analysis.png")

if __name__ == '__main__':
    main()
