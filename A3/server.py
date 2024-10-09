#!/usr/bin/env python3
import argparse
import iperf3 
import threading

def run_server(ip, port):
    server = iperf3.Server()
    server.bind_address = ip
    server.port = port
    # run the server
    server.run()

def main():
    parser = argparse.ArgumentParser(description='Process server parameters')
    parser.add_argument("-ip", help = "accepts the ip address from command line", required=True)
    parser.add_argument("-port", type=int, help = "accepts port from command line", required=True)
    args = parser.parse_args()
    server_args = vars(args)

    run_server(server_args["ip"], server_args["port"])

if __name__ == '__main__':
    main()
