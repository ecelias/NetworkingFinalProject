<strong>Assignment 3 for CS3640</strong> <br>
<em>Group members:</em>
<ul>
<li>Madeline Harbaugh (mharbaugh)
<li> Kristin To (kto)
<li>Elizabeth Elias (ecelias)
<li>Maria Gauna (mgauna)
</ul>
<em>Code Test Run Instructions:</em> <br>
In order to run this code, please ensure that you have Mininet and iPerf properly installed. <br> 
You can check this by running: <br>
<code>sudo mn --version</code> <br>
<code>pip show iperf3</code> <br> <br>
All functionality needed to run iPerf tests on a Mininet object can be accessed from <code>network_bottleneck.py</code>, you should not need to enter the <code>server.py</code> or <code>client.py</code> scripts. <br> 
<br> Begin by navigating to to A3 directory. <br> <br>
The virtual environment used to create this code should be stored in the repository and can be activated with: <br>
<code> source ~/cs3640/A3/bin/activate </code> <br>
Open a bash terminal and run the following command: <br>
<code>sudo mn -c</code> <br>
This will ensure that the Mininet's network is clear and prevent errrors in creation and configuration of a new network.<br>
Then, run the following command: <br>
<code>sudo python3 network_bottleneck.py -bw_other {non-bottleneck links bandwidth} -bw_bottleneck {bottleneck link bandwidth} -time {duration of traffic stimulation}</code> <br> 
You must prepend this command with <code>sudo</code> as mininet must run from root. <br> <br>
If you run into errors using <code>network_bottleneck.py</code>, you can take the following steps to ensure <code>server.py</code> and <code>client.py</code> are running correctly. <br> 
Open a bash terminal and run: <br>
<code>python3 server.py -ip {ip_address} -port {port_number}</code> <br>
Then, in a new bash terminal, run: <br>
<code>python3 client.py -ip {client ip address} -port {port_number} -server_ip {ip address of server} -test {network protocol}</code> <br>
<br>
You can run <code>analyze_perf.py</code> and get the network analysis in one of two ways. <br>
(1) Press "Run Python File" in vscode <br>
(2) Open a new bash terminal and run: <br>
<code>python3 analyze_perf.py</code> <br> <br>
<strong>Credit Reel:</strong> <br>
<em>Madeline Harbaugh (mharbaugh) contributions:</em> <ul>
<li> Completed Task 3:  Analyzing Network Performance 
</ul>
<em>Kristin To (kto) contributions: </em> <ul>
<li> Completed Task 1:  Creating a network topology in Mininet
</ul>
<em>Elizabeth Elias (ecelias) contributions: </em> <ul>
<li> Did part of Task 2:  Simulating Traffic with iPerf, including: <ul>
<li> Installing iPerf3 and it’s Python bindings.
<li> Wrote <code>run_perf_tests()</code>
<li> Wrote the ReadMe Instructions
</ul>
</ul>
<em>Maria Gauna (mgauna) contributions: </em> <ul>
<li> Did part of Task 2: Simulating Traffic with iPerf, including: <ul>
<li> Creating iPerf clients. 
<li> Creating iPerf servers.
<li> Wrote the ReadMe Credit Reel
</ul>
</ul>

<ul>
<li> [Mininet definitions and implementation](https://mininet.org/api/classmininet_1_1node_1_1Node.html)
<li> [Plotting with Python](https://www.w3schools.com/python/matplotlib_pyplot.asp)
<li> [iPerf implementation](https://iperf.fr/iperf-doc.php#3doc)
<li> [iPerf implementation](https://iperf3-python.readthedocs.io/en/latest/modules.html)
<li> [iPerf and Mininet Debugging](https://github.com/mininet/mininet/tree/master/examples)
<li> [Anonymous Post on this Piazza Post for iPerf Debugging](https://piazza.com/class/m03njulygss731/post/60)
<li> [Used this to find the default byte length of a packet](https://iperf.fr/iperf-doc.php#:~:text=read%20or%20write.-,iPerf%20works%20by%20writing%20an%20array%20of%20len%20bytes%20a,TCP%2C%201470%20bytes%20for%20UDP.)
<li> [Implemention of mathplotlib](https://www.geeksforgeeks.org/data-visualization-using-matplotlib/)
</ul>