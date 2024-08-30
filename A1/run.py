import subprocess as sp 
import sys
# Used https://www.geeksforgeeks.org/python-subprocess-module/ to learn about the subprocess module 

file1 = open('/home/ecelias/cs3640/A1/output.txt', 'w+')
file1.write('ecelias Elizabeth Elias')
file1.write('\n')
file1.write('\n')


def to_output_file(new_line):
    file1.write('\n*****\n')
    file1.write(new_line)
        
if len(sys.argv) == 2:
    ip_address = sys.argv[1]
    print(ip_address)
    
    try:
        current_date = sp.run(['date'], capture_output=True, text=True)
        to_output_file(f'Command: <date> {current_date.stdout}')
    except sp.CalledProcessError as e:
        to_output_file(f'[Error] Command: <date> failed with return code: {e.returncode}')
        print(f'[Error] Command <date> failed with return code: {e.returncode}')
    
    try:
        current_user = sp.run(['whoami'], capture_output=True, text=True)
        to_output_file(f'Command: <whoami> {current_user.stdout}')
    except sp.CalledProcessError as e:
        to_output_file(f'[Error] Command: <whoami> failed with return code: {e.returncode}')
        print(f'[Error] Command <whoami> failed with return code: {e.returncode}')
    
    try:
        current_ifconfig = sp.run(['ifconfig'], capture_output=True, text=True)
        to_output_file(f'Command: <ifconfig> {current_ifconfig.stdout}')
    except sp.CalledProcessError as e:
        to_output_file(f'[Error] Command: <ifconfig> failed with return code: {e.returncode}')
        print(f'[Error] Command <ifconfig> failed with return code: {e.returncode}')
            
    try:
        current_ping = sp.run(['ping', ip_address, '-c', '10'], capture_output=True, text=True)
        to_output_file(f'Command: <ping {ip_address} -c 10> {current_ping.stdout}')
    except sp.CalledProcessError as e:
        to_output_file(f'[Error] Command: <ping {ip_address} -c 10> failed with return code: {e.returncode}')
        print(f'[Error] Command <ping {ip_address} -c 10> failed with return code: {e.returncode}')
                    
    try:
        current_trace = sp.run(['traceroute', ip_address, '-m', '10'], capture_output=True, text=True)
        to_output_file(f'Command: <traceroute> {ip_address} -m 10> {current_trace.stdout}')
    except sp.CalledProcessError as e:
        to_output_file(f'[Error] Command: <traceroute> {ip_address} -m 10> failed with return code: {e.returncode}')
        print(f'[Error] Command <traceroute> {ip_address} -m 10> failed with return code: {e.returncode}')
    

file1.close()