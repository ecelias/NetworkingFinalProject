<h2>Instructions for performing the data</code></h2>

<h3>Converting HTML files to plaintext</h3>

<h5>Installing dependencies</h5>
Clone in the following repository: <code>git clone https://github.com/benandow/HtmlToPlaintext</code> and navigate to the directory <code>cd ~/HtmlToPlaintext</code>. <br> <br>

You will need the following libraries to generate visualizations for the data:<ul>
<li>pandas
<li>seaborn
<li>matplotlib
<li>numpy
<li>statistics
</ul>

Make the following directories inside HtmlToPlaintext: <code>./ext/html_policies</code> and <code>./ext/plaintext_policies</code> <br><br>
Install and run docker with the [setup guide](https://docs.docker.com/engine/install/ubuntu/) 

<h5>Running HtmlToPlaintext</h5>
Ensure all html files are located in <code>cd ~/HtmlToPlaintext/ext/html_policies</code> <br><br>
In the terminal, navigate to <code>cd ~/HtmlToPlaintext</code>. <br><br>
In the terminal run, <code>sudo ./build.sh </code><br><br>
In the terminal run, <code>sudo ./run.sh </code><br><br>
All HTML files should now be located in <code>./ext/plaintext_policies</code> as plaintext files.

<h5>Running HtmlToPlaintext</h5>


<h5>Resources</h5>
<ul>
<li>[HtmlToPlaintext](https://github.com/benandow/HtmlToPlaintext)
<li>[Docker Installation](https://docs.docker.com/engine/install/ubuntu/)
<li>
</ul>