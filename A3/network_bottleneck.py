#!/usr/bin/env python3                                                                                                                                                                
from mininet.topo import Topo  
from mininet.net import Mininet  
from mininet.node import CPULimitedHost
from mininet.node import Host, Controller, OVSController, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel   
import argparse
import subprocess
import json
import time

f = open("output-network-config.txt", "w+")


class BottleneckTopo(Topo):
    #"Single switch connected to n hosts."  
    def build(self, bw_bottleneck, bw_other):
        # Topo.build(self)
        h1= self.addHost( 'h1', ip='10.0.0.1' )
        h2 = self.addHost( 'h2', ip='10.0.0.2' )
        h3 = self.addHost( 'h3', ip='10.0.0.3' )
        h4 = self.addHost( 'h4', ip='10.0.0.4' )
        
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        
        self.addLink(h1,s1, bw=bw_other)
        self.addLink(h2,s1,bw =bw_other)
        self.addLink(s1,s2, bw=bw_bottleneck) #bottleneck link
        self.addLink(s2,h3, bw=bw_other)
        self.addLink(s2,h4, bw =bw_other)

# validates user input
def validateInput(validInt, bw_bottleneck, bw_other, time):
   while validInt == False:
        try:
            isinstance(bw_bottleneck, int)
        except ValueError:
            print("Please enter a valid integer for -bw_bandwidth.")
            continue
        try:
           isinstance(bw_other, int)
        except ValueError:
            print("Please enter a valid integer for -bw_other.")
            continue
        try:
           isinstance(time, int)
        except ValueError:
            print("Please enter a valid integer for -time.")
            continue
       
        if bw_bottleneck < 0 | bw_other < 0:
            print("Sorry, your response must not be negative. Please try again")
            continue

        if bw_bottleneck >= bw_other:
            print("Bottleneck bandwidth must be less than other bandwidth. Please try again. ")
            continue
        else:
            #bw was successfully parsed
            print("Valid inputs. Starting network stimulation tests.")
            validInt = True
            return validInt

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
    # ???? modified for testing purposes because I didn't have cgroup v1 mounted and didn't want to do that right now
    net = Mininet(topo=topo, host=Host, link=TCLink)
    net.start()
    print( "Dumping host connections" )
    dumpNodeConnections(net.hosts)

    # call the method to write the "ifconfig" command on all hosts to a file
    call_ifconfig(net)

    # ???? commented out for now MAKE USRE TO UNCOMMENT BEFORE SUBMISSION
    call_ping(net)

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
    # initialize a topo and mininet object
    topo = BottleneckTopo(bw_bottleneck=bw_bottleneck, bw_other=bw_other)
    net = Mininet(topo=topo, host=Host, link=TCLink)
    net.start()

    # dump host connections, will help check if mininet was created correctly 
    print( "Dumping host connections" )
    dumpNodeConnections(net.hosts)

    # get all of the hosts from the network 
    h1 = net.get("h1")
    h2 = net.get("h2")
    h3 = net.get("h3")
    h4 = net.get("h4")

    # initiliaze a tcp server on the h3 node
    tcp_server = h3.cmd('sudo python3 server.py -ip 10.0.0.3 -port 5201 &')
    # run the tcp test on the h1 node
    tcp_test = h1.cmd('sudo python3 client.py -ip 10.0.0.1 -port 5201 -server_ip 10.0.0.3 -test tcp')

    # configure info as dictionary to dump into json file for the tcp tests
    # ???? this needs to be formatted correctly
    tcp_results = {
        "tcp_test": "tcp",
        "tcp_bottleneck_bw": bw_bottleneck, 
        "tcp_other_bw": bw_other, 
        "tcp_bytes_sent": tcp_test,
        "tcp_bytes_received": "please say this works"
        }
    
    # dump test info into tcp json file
    with open(f"output-tcp-{bw_bottleneck}-{bw_other}.json", "w") as tcp_file:
            json.dump(tcp_results, tcp_file, indent=6)               
    
    # initiliaze a udp server on the h4 node
    udp_server = h4.cmd('sudo python3 server.py -ip 10.0.0.4 -port 5202 &')
    # run the tcp test on the h1 node
    udp_test = h2.cmd('sudo python3 client.py -ip 10.0.0.2 -port 5202 -server_ip 10.0.0.4 -test udp')
    print(udp_test)

    # configure info as dictionary to dump into json file for the udp tests
    # ???? this needs to be formatted correctly
    udp_results = {
        "udp_test": "udp",
        "udp_bottleneck_bw": bw_bottleneck, 
        "udp_other_bw": bw_other, 
        "udp_bytes_sent": udp_test,
        "udp_bytes_received": "please say this works"
        }
    
    # dump test info into udp json files
    with open(f"output-udp-{bw_bottleneck}-{bw_other}.json", "w") as udp_file:
            json.dump(udp_results, udp_file, indent=6)               


def main():
    #take in arguments
    parser = argparse.ArgumentParser(description ='Process parameters' )
    parser.add_argument('-bw_other', type=int, default=100)
    parser.add_argument('-time', type=int, default=10)
    parser.add_argument('-bw_bottleneck', type=int, default=10)
    args = parser.parse_args()

    # get bottleneck bandwidth and other bandwidth from command line inputs       
    bw_bottleneck = args.bw_bottleneck
    bw_other = args.bw_other
    time = args.time
    
    # Tell mininet to print useful information
    setLogLevel('info')
    validInt = False
    while validInt ==  False: 
        if (bw_bottleneck) < (bw_other):
            if (isinstance(bw_bottleneck, int)) and (isinstance(bw_other, int) and isinstance(time, int)):
                validInt = validateInput(validInt, bw_bottleneck, bw_other, time)
    #run_topology_tests(bw_bottleneck, bw_other) 
    run_perf_tests(bw_bottleneck, bw_other)

if __name__ == '__main__':
    main()

f.close()
