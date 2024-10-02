#!/usr/bin python                                                                                                                                                                     
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.node import Host
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import argparse
import subprocess
import json

validInt = False

f = open("output-network-config.txt", "w+")


class BottleneckTopo(Topo):
    #"Single switch connected to n hosts."  
    def build(self, bw_bottleneck, bw_other):
        # Topo.build(self)
        client1= self.addHost('h1')
        client2 = self.addHost('h2')
        server1 = self.addHost('h3')
        server2= self.addHost('h4')
        
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        
        self.addLink(client1,switch1, bw=bw_other)
        self.addLink(client2,switch1,bw =bw_other)
        self.addLink(switch1,switch2, bw=bw_bottleneck) #bottleneck link
        self.addLink(switch2,server1, bw=bw_other)
        self.addLink(switch2,server2, bw =bw_other)

# method to call the ifconfig commands on all hosts in a mininet object and write the output to a file
def call_ifconfig(mininetObj):
    for host in mininetObj.hosts:
        host_file = open(f"output-ifconfig-{host}.txt", "w+")
        current_host_config = host.cmd('ifconfig')
        host_file.write(current_host_config)

# method to call the ping commands on all hosts in a mininet object and write the output to a file
# ???? this method takes a while to run, maybe there's a way to speed it up
# ???? i commented out this method call in the "run_topology_tests" for now bc it takes a decent chunk of time to run
def call_ping(mininetObj):
    for src in mininetObj.hosts:
        host_file = open(f"output-ping-{src}.txt", "w+")
        for dest in mininetObj.hosts:
            if src != dest:
                dest_ip = dest.IP()
                command = ['ping', dest_ip, '-c', '10']
                current_host_ping = src.cmd(command)
                host_file.write(f'Ping from {src.name} to {dest.name}\n')
                host_file.write(current_host_ping)


#should be called by main
#need to add error handling if user doesn't input a valid int
def run_topology_tests(bw_bottleneck, bw_other):
    #"Create and test a simple network"
    # ???? not sure how to use BottleneckTopo.build() here but instructions say we should
    topo = BottleneckTopo(bw_bottleneck=bw_bottleneck, bw_other=bw_other)

    # net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    # modified for testing purposes because I didn't have cgroup v1 mounted and didn't want to do that right now
    net = Mininet(topo=topo, host=Host, link=TCLink)

    net.start()
    print( "Dumping host connections" )
    dumpNodeConnections(net.hosts)

    # call the method to write the "ifconfig" command on all hosts to a file
    call_ifconfig(net)

    # ???? commented out for now MAKE USRE TO UNCOMMENT BEFORE SUBMISSION
    #call_ping(net)

    # write details of hosts, switches, and links to output-network-config.txt file
    # ???? may need more info here?? I'm unsure of what "details" all need to be written
    f.write("Nodes:\n")
    for host in net.hosts:
        f.write(f"  -Host: {host.name}\n")
    for switch in net.switches:
        f.write(f"  -Switch: {switch.name}\n")
    f.write("Links:\n")
    for link in net.links:
        f.write(f"  -Link: {link}\n")

    print( "Testing network connectivity" )
    net.pingAll()
    net.stop()
    
    # ???? sorry couldn't figure out how to make this functional 
    #runTopOutput = subprocess.BottleneckTopo.build(bw_bottleneck, bw_other)
    #f.write(runTopOutput)

# should be called by main
def run_perf_tests(bw_bottleneck, bw_other):
    # command line inputs to run the iperf tests
    tcp_test_command = "python3 client.py -ip h1 -port 5000 -server_ip h3 -test tcp"
    udp_test_command = "python3 client.py -ip h2 -port 5000 -server_ip h4 -test udp" 

    # run the tcp and udp tests
    tcp_test = subprocess.run(tcp_test_command, shell=True, capture_output=True, text=True)
    udp_test = subprocess.run(udp_test_command, shell=True, capture_output=True, text=True)

    # capture bytes sent and recieved by each test
    tcp_bytes_sent = tcp_test.sent_bytes
    tcp_bytes_recv = tcp_test.recieved_bytes

    # udp test doesn't have parameters for sent and recieved bytes
    # will need to manually calculate but this will server as a placeholder for now
    udp_bytes_sent = udp_test.bytes
    udp_bytes_recv = udp_test.bytes

    # configure info as dictionary to dump into json file for both tests
    tcp_results = {
        "tcp_test": "tcp",
        "tcp_bottleneck_bw": bw_bottleneck, 
        "tcp_other_bw": bw_other, 
        "tcp_bytes_sent": tcp_bytes_sent,
        "tcp_bytes_received": tcp_bytes_recv
    }

    udp_results = {
        "udp_test": "udp",
        "udp_bottleneck_bw": bw_bottleneck, 
        "udp_other_bw": bw_other, 
        "udp_bytes_sent": udp_bytes_sent,
        "udp_bytes_received": udp_bytes_recv
    }

    # dump test info into respective json files
    with open(f"output-tcp-{bw_bottleneck}-{bw_other}.json", "w") as tcp_file:
        json.dump(tcp_results, tcp_file, indent=6)
    with open(f"output-udp-{bw_bottleneck}-{bw_other}.json", "w") as udp_file:
        json.dump(udp_results, udp_file, indent=6)

    
def main():
    #take in arguments
    parser = argparse.ArgumentParser(description ='Process parameters' )
    parser.add_argument('-bw_other', type=int, default=100)
    parser.add_argument('-time', default = 10)
    parser.add_argument('-bw_bottleneck', type=int, default=10)
    args = parser.parse_args()
    args_dict = vars(args)

    # get bottleneck bandwidth and other bandwidth from command line inputs       
    bw_bottleneck = args.bw_bottleneck
    bw_other = args.bw_other
    
    # Tell mininet to print useful information
    setLogLevel('info')
    run_topology_tests(bw_bottleneck, bw_other) 
    validInt = False
    while validInt ==  False: 
        if (bw_bottleneck) < (bw_other):
            if (isinstance(bw_bottleneck, int)) and (isinstance(bw_other, int)):
                validInt = True


if __name__ == '__main__':
    main()

f.close()
