<h1><strong>CS3640 Assignment 4</strong></h1> <br>
<h4><strong>Instructions for running assignment 4</strong></h4> <br>
In order to run this code, make sure you have dpkt, dnspython python-whois, ipwhois, OpenSSl  properly installed. <br>
You can check this by running: <br>
<code>pip install dpkt</code> <br>
<code>pip install OpenSSl</code> <br>
<code>pip install dnspython python-whois</code> <br> 
<code>pip install ipwhois</code> <br> <br>
<br> Begin by navigating to to A4 directory. <br> <br>
The virtual environment used to create this code should be stored in the repository and can be activated with: <br>
<code> source ~/cs3640/A4/bin/activate </code> <br>
Remember before running any commands in the terminals for all the code except for the server you need to prepend the command with <code>sudo</code> as you need to run with the administrative privilages to run raw sockets, as send and recieving ICMP packets are generally restricted to elevated permissions. <br>
Also after inputting a sudo command, remember you might have to input your computer password. <br>
For testing cs3640-ping.py: <br>
Open a bash terminal and run the following command: <br>
<code>python3 cs3640-ping.py -destination {IP Address Destination} -n {Number of packets you want to send} -ttl {Time-to-Live for the ICMP packet} </code> <br>
Then, to test cs3640-traceroute run the following command: <br>
<code>python3 cs3640-traceroute.py -destination {IP Address Destinaton} -n_hops {number of hops}</code> <br> 
<br> Finally, to test the intelligence server and client: <br> <br>
(1)Open a bash terminal, and run the following command: 
<code> python cs3640-intelserver.py </code> <br>
(2) open a new bash terminal and run the following command: 
<code> python3 cs3640-intelclient.py -domain {Insert domain to query} -service {The service you want to run}</code> <br>
You can run this command as many times as you want with all different domaians and services through the server. <br> <br>

<code>python3 analyze_perf.py</code> <br> <br>
<h4><strong>Group Members</strong></h4> <ul>
<li> Elizabeth Elias, ecelias
<li> Maria Gauna, mgauna
<li> Madeline Harbaugh, mharbaugh
<li> Kristin To, kto
</ul>

<h4><strong>Group Member Contributions</strong></h4> <ul>
<strong>Credit Reel:</strong> <br>
<em>Madeline Harbaugh (mharbaugh) contributions:</em> <ul>
<li> Completed Task 2: Implementing the Traceroute Program.
</ul>
<em>Kristin To (kto) contributions: </em> <ul>
<li> Completed Task 1: Implementing the Ping Program.
</ul>
<em>Elizabeth Elias (ecelias) contributions: </em> <ul>
<li> Did part of Task 3: Implementing the Intelligence Server and Client, including: <ul>
<li> Programmed intelligence server overview (cs3640-intelserver.py) except for IPV6_ADDR and IPV4_ADDR methods.
<li> Wrote the ReadMe Instructions.
</ul>
</ul>
<em>Maria Gauna (mgauna) contributions: </em> <ul>
<li> Did part of Task 3: Implementing the Intelligence Server and Client, including: <ul>
<li> Programmed intelligence client overview.(cs3640-intelclient.py) and the methods IPV6_ADDR and IPV4_ADDR (cs3640-intelserver.py).
<li> Wrote the ReadMe Credit Reel.
</ul>
</ul>

<h4><strong>Credit Reel:</strong></h4> <ul>
<li>[Creating an ICMP server in Python](https://stackoverflow.com/questions/8245344/python-icmp-socket-server-not-tcp-udp)
<li>[ICMP Echo DPKT Tutorial](https://jon.oberheide.org/blog/2008/08/25/dpkt-tutorial-1-icmp-echo/)
<li>[Running a ping command with an ICMP server and checksum calculator](https://github.com/WarlonZeng/CS4793-Computer-Networking/blob/master/python%20icmp%20traceroute/icmp_pinger.py)
<li>[Running a ping command with an ICMP server](https://github.com/insomniacslk/dpkt/blob/master/examples/ping.py)
<li>[Client-Server IP addressal retrieval and response](https://www.geeksforgeeks.org/network-programming-in-python-dns-look-up/)
<li>[Client-Server TSL/SSL certificate retrieval and response](https://pythontic.com/ssl/sslsocket/getpeercert)
<li>[Client-Server hosting AS information](https://stackoverflow.com/questions/28997623/how-to-parse-text-in-python-with-ipwhois)
<li>[Getting TLS Certificate Information](https://stackoverflow.com/questions/7689941/how-can-i-retrieve-the-tls-ssl-peer-certificate-of-a-remote-host-using-python)
</ul>