<h1><strong>CS3640 Assignment 5</strong></h1> <br>
<h2>To run <code>crawler.py</code></h2>

<h4>Activate the environment</h4> 
In the <code>~/cs3640</code> directory, run <code>source ~/cs3640/A3/bin/activate</code>

<h4>Install dependencies</h4> 
<strong>Installing Playwright</strong> <br>
Install Playwright with <code>pip install pytest-playwright</code>. <br>
Then install the required playwright browsers with <code>playwright install</code>. <br>
You may need to also run <code>sudo apt-get install libasound2t64</code>. <br> <br>

<strong>Installing BeautifulSoup</strong> <br>
Install BeautifulSoup4 with <code>pip install beautifulsoup4</code>. <br><br>

<strong>Installing requests</strong> <br>
Install requests with <code>pip install requests</code>. 

<h4>Run Crawler.py</h4> 
Navigate to the <code>cd ~/cs3640/A5/crawler</code> directory and run <code>python3 crawler.py</code> in the terminal. <br>Alternatively, you can run <code>python3 crawler/crawler.py</code> in the terminal from the <code>~/cs3640/A5</code> directory.


<h4>Resources</h4>
<ul>
<li>[Using BeautifulSoup](https://oxylabs.io/blog/beautiful-soup-parsing-tutorial)
<li>[BeautifulSoup find_all method](https://scrapeops.io/python-web-scraping-playbook/python-beautifulsoup-findall/)
<li>[Using Playwright](https://www.roborabbit.com/blog/web-scraping-with-playwright-in-python/)
</ul>

<h2>Instructions for converting the data</code></h2>

<h3>Converting HTML files to plaintext</h3>

<h5>Installing dependencies</h5>
Clone in the following repository: <code>git clone https://github.com/benandow/HtmlToPlaintext</code> and navigate to the directory <code>cd ~/HtmlToPlaintext</code>. <br> <br>

Make the following directories inside HtmlToPlaintext: <code>./ext/html_policies</code> and <code>./ext/plaintext_policies</code> <br><br>
Install and run docker with the [setup guide](https://docs.docker.com/engine/install/ubuntu/) 

<h5>Running HtmlToPlaintext</h5>
Ensure all html files are located in <code>cd ~/HtmlToPlaintext/ext/html_policies</code> <br><br>
In the terminal, navigate to <code>cd ~/HtmlToPlaintext</code>. <br><br>
In the terminal run, <code>sudo ./build.sh </code><br><br>
In the terminal run, <code>sudo ./run.sh </code><br><br>
All HTML files should now be located in <code>./ext/plaintext_policies</code> as plaintext files.


<h5>Resources</h5>
<ul>
<li>[HtmlToPlaintext](https://github.com/benandow/HtmlToPlaintext)
<li>[Docker Installation](https://docs.docker.com/engine/install/ubuntu/)
</ul>

<h4><strong>Group Members</strong></h4>

 Elizabeth Elias, <em>ecelias</em> <br>

 Maria Gauna, <em>mgauna</em> <br>

 Madeline Harbaugh, <em>mharbaugh</em> <br>

 Kristin To, <em>kto</em> <br>


<h4><strong>Group Member Contributions</strong></h4><br>

Madeline Harbaugh (mharbaugh) contributions:<br>
<ul>
<li>Madeline read and created presentation slides concerning research papers one and two.
<li>Madeline created and read out introduction presentation slide
</ul>
 



Kristin To (kto) contributions:<br>
<ul>
<li>Kristin read and created presentation slides concerning research paper three.
<li>Kristin created and read out research question 1 presentation slide 
</ul>




Elizabeth Elias (ecelias) contributions:<br>
<ul>
<li>Liz read and created presentation slides concerning research paper four.
<li>Liz created and read out research question 2 presentation slide 
</ul>


Maria Gauna (mgauna) contributions:<br>
<ul>
<li>Maria read and created presentation slides concerning research paper five.
<li>Maria created and read out research question 3 presentation slide 
<li>Wrote A5/README.md
</ul>




Data:<br>
<ul>
<li> DNSMPI_Files (gives all the DSNMPI files for the websites) and html_policies (gives all the html_policies) are under data folder in A5 and give the data we scraped from the websites privacy policies information.
<li>csvData.csv is a running csv file that updates after each crawler.py call with all the information scraped from our crawler.py.
<li> FinalTableData.csv is a final csv file that we ran from our crawler that we based all out statistics and analysis off of.
<ul>
<li> It sorts all the information into eight categories, titled: Website,Number of Pages,Number of Cookies,Contains DNSMPI-associated Content?,DNSMPI Content,Cookie Information,HTTP/HTTPS Policies Category,Mixed Content
</ul>
<li> a5-video.mp4 gives the video presentation of our reserach questions and findings from the papers 

</ul>

<h4><strong>Credit Reel:</strong></h4> <br>
<ul>
<li> - Resources listed above -
<li> - Assigned readings from class - 
<li>[Analysis Paper Context Information](https://www.pewresearch.org/short-reads/2023/11/22/online-shopping-has-grown-rapidly-in-u-s-but-most-sales-are-still-in-stores/)
<li>[Data Modeling](https://www.w3schools.com/python/matplotlib_pyplot.asp)
</ul>