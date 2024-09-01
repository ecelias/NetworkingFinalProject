import subprocess as sp 
import sys
# Used https://www.geeksforgeeks.org/python-subprocess-module/ to learn about the subprocess module and the syntax for the try-except blocks

file1 = open('/home/ecelias/cs3640/A1/output.txt', 'w+')
file1.write('ecelias Elizabeth Elias')
file1.write('\n')
file1.write('\n')

def to_output_file(new_line):
    file1.write('\n*****\n')
    file1.write(new_line)
    
        
if len(sys.argv) == 2:
    ip_address = sys.argv[1]
    
    commands = [
    ['date'],
    ['whoami'],
    ['ifconfig'],
    ['ping', ip_address, '-c', '10'],
    ['traceroute', ip_address, '-m', '10'],
    ]  
    
    for command in commands:
        try:
            current_command = sp.run(command, capture_output=True, text=True)
            to_output_file(f'Command: <{command}> {current_command.stdout}')
        except sp.CalledProcessError as e:
            to_output_file(f'[Error] Command: <{command}> failed with return code: {e.returncode}')
            print(f'[Error] Command <{command}> failed with return code: {e.returncode}')

elif len(sys.argv) == 2:
    to_output_file('[Error] No IP address found in system input. Please try again.')
    print('[Error] No IP address found in system input. Please try again.')
    
elif len(sys.argv) > 2:
    to_output_file('[Error] Too many arguments detected. Please try again.')
    print('[Error] No IP address found in system input. Please try again.')

elif len(sys.argv) < 1:
    to_output_file('[Error] Script name and IP address not defined. Please try again.')
    print('[Error] Script name and IP address not defined. Please try again.')

file1.close()