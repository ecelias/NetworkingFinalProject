## network_bottleneck

#!/usr/bin/python                                                                            
                                                                                             
import Topo
import Mininet
import dumpNodeConnections
import setLogLevel
import argparse
import subprocess

validInt = False

f = open("output-network-config.txt", "a")


class BottleneckTopo():
    "Single switch connected to n hosts."
    def build(self, bw_bottleneck, bw_other):
        Topo.build(self)
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

#should be called by main
#need to add error handling if user doesn't input a valid int
def run_topology_tests(bw_bottleneck, bw_other):
    "Create and test a simple network"
    topo = BottleneckTopo()
    net = Mininet (topo=topo,
	           host=CPULimitedHost, link=TCLink )
    net.start()
    print( "Dumping host connections" )
    dumpNodeConnections(net.hosts)
    print( "Testing network connectivity" )
    net.pingAll()
    net.stop()

    runTopOutput = subprocess.BottleneckTopo.build(bw_bottleneck, bw_other)
    f.write(runTopOutput)
    #details of configuration write to output-network-config.txt
    
def main():
    #take in arguments
    parser = argparse.ArgumentParser(description ='Process parameters' )
    parser.add_argument('-bw_other', default=100)
    parser.add_argument('-time', default = 10)
    parser.add_argument('–bw_bottleneck', default=10)

    # Tell mininet to print useful information
    setLogLevel('info')
    run_topology_tests(bw_bottleneck, bw_other) 
    while validInt ==  False: 
        print('Enter bandwidth of the bottleneck link (in Mbps): ')
        -bw_bottleneck = input()
        print('Enter bandwidth of the other links (in Mbps): ')
        -bw_other = input()
        if (-bw_bottleneck) < (-bw_other):
            if (type(-bw_bottleneck)) and (type(-bw_other)) == '<class 'int'>':
                validInt = True



if __name__ == '__main__':
    main()

f.close()
