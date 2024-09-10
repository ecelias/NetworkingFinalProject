Assignment 2 Instructions:
Instructions to run client.py and server.py for assignment 2
Navigate to the directory containing the server.py and client.py files 
Choose a port number that exceeds 1023. This will be referred to as <PORT_NUM>

In a new terminal window, run: python3 server.py <PORT_NUM>
For each new client you wish to open, open a new terminal window and run: python3 client.py localhost <PORT_NUM>
Make sure the port number for all clients you wish to connect to the same server matches the port for the server. 

You will be prompted to enter a message you wish to send to the server. To quit, type "/quit" or press (Ctrl + C). 


Resources:
<br>
Basic syntax for socket programming:
https://www.geeksforgeeks.org/socket-programming-python/ 

Multi-threading syntax (in the context of socket programming):
https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
https://www.tutorialspoint.com/socket-programming-with-multi-threading-in-python 
https://github.com/MattCrook/python_sockets_multi_threading 

Sending/receiving messages for multiple clients:
https://stackoverflow.com/questions/27139240/i-need-the-server-to-send-messages-to-all-clients-python-sockets


