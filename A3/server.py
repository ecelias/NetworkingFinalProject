import argparse
import iperf3 

parser = argparse.ArgumentParser(description='Process server parameters')
parser.add_argument("-ip", help = "accepts the ip address from command line", required=True)
parser.add_argument("-port", help = "accepts port from command line", required=True)
args = parser.parse_args()
server_args = vars(args)

server = iperf3.Server()
server.bind_address = server_args["ip"]
server.port = server_args["port"]
server.verbose = False
while True:
    server.run()

