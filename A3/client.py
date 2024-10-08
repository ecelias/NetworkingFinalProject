#!/usr/bin/env python3
import argparse 
import iperf3

def run_client(client_args):
    client= iperf3.Client()
    client.duration = client_args["duration"]
    client.bind_address = client_args["ip"]
    client.server_hostname = client_args["server_ip"]
    client.port = client_args["port"]
    client.json_output = client_args["json_output"]
    client.protocol = client_args["test"]

    client_result = client.run()
    if client_result.error:
        print(f"Error running iperf3 client: {client_result.error}")
    else:
        print(f"Test successful: {client_result}")
    return client_result


def main():
    parser = argparse.ArgumentParser(description='Process client parameters')
    parser.add_argument("-ip", help = "accepts the ip address from command line", required=True)
    parser.add_argument("-port", type=int, help = "accepts port from command line", required=True)
    parser.add_argument("-server_ip", help = "accepts server IP address from command line", required=True)
    parser.add_argument("-test", help = "accepts type of test client server from command line", required=True)
    ## will default the duration to 60 seconds but can be altered in command line
    ## ???? make sure you change this back to 60
    parser.add_argument("-duration", default=60)
    ## can use the command line to not create a JSON output but will default to have JSON output when unspecified
    parser.add_argument("-json_output", type=bool, default=True)
    args = parser.parse_args()
    ## adds all arguments from arg paraser to a dictionary for easy access
    client_args = vars(args)

    result = run_client(client_args)
    print(result.protocol)
    return result

if __name__ == '__main__':
    main()
