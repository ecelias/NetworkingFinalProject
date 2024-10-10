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

    # run the client server
    client_result = client.run()

    # if an error occurs, throw an exception 
    if client_result.error:
        raise Exception(f"An error occured. {client_result.error}")
    else:
        # if the test type is tcp, get the sent_bytes and received bytes from the TestResult object
        if client_args["test"] == "tcp":
            print(client_result.sent_bytes, client_result.received_bytes, client_result.duration)
        # if the test type is udp, get the sent_bytes and received bytes from the TestResult object
        elif client_args["test"] == "udp": 
            print(client_result.bytes, client_result.duration)
        # if the test type is not TCP or UDP, throw an exception and exit the client
        else:
            raise Exception(f"Invalid test type used. Exiting program...")
    return client_result


def main():
    parser = argparse.ArgumentParser(description='Process client parameters')
    parser.add_argument("-ip", help = "accepts the ip address from command line", required=True)
    parser.add_argument("-port", type=int, help = "accepts port from command line", required=True)
    parser.add_argument("-server_ip", help = "accepts server IP address from command line", required=True)
    parser.add_argument("-test", type=str, help = "accepts type of test client server from command line", required=True)
    ## will default the duration to 60 seconds but can be altered in command line
    parser.add_argument("-duration", type=int, default=60)
    ## can use the command line to not create a JSON output but will default to have JSON output when unspecified
    parser.add_argument("-json_output", type=bool, default=True)
    args = parser.parse_args()
    ## adds all arguments from arg paraser to a dictionary for easy access
    client_args = vars(args)

    # call the function to run the client
    result = run_client(client_args)
    return result

if __name__ == '__main__':
    main()
