<h1>Final Group project for CS3640</h1>
<h4>This project required all group members to demonstrate a capability to develop a web scraper and analyze the data in alignment with good software development practices. </h4>

<h4><strong>Group Members</strong></h4>

 Elizabeth Elias<br>

 Maria Gauna<br>

 Madeline Harbaugh<br>

 Kristin To<br>

<h1><strong>CS3640 Assignment 5</strong></h1>
<h2>To run <code>crawler.py</code></h2>

<h4>Activate the environment</h4> 
In the <code>~/cs3640</code> directory, run <code>source ~/cs3640/A3/bin/activate</code>

<h4>Install dependencies</h4> 
<strong>Installing Playwright</strong> <br>
Install Playwright with <code>pip install pytest-playwright</code>. <br>
Then install the required playwright browsers with <code>playwright install</code>. <br>
You may need to also run <code>sudo apt-get install libasound2t64</code>. <br> <br>

<strong>Installing BeautifulSoup</strong> <br>
Install BeautifulSoup4 with <code>pip install beautifulsoup4</code>. <br>

<strong>Installing requests</strong> <br>
Install requests with <code>pip install requests</code>. 

<h4>Run Crawler.py</h4> 
Navigate to the <code>cd ~/cs3640/A5/crawler</code> directory and run <code>python3 crawler.py</code> in the terminal. <br>Alternatively, you can run <code>python3 crawler/crawler.py</code> in the terminal from the <code>~/cs3640/A5</code> directory.

<h4>Resources</h4>
[Using BeautifulSoup](https://oxylabs.io/blog/beautiful-soup-parsing-tutorial)
[BeautifulSoup findall method](https://scrapeops.io/python-web-scraping-playbook/python-beautifulsoup-findall/) 
[Using Playwright](https://www.roborabbit.com/blog/web-scraping-with-playwright-in-python/) 


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

[HtmlToPlaintext](https://github.com/benandow/HtmlToPlaintext)
[Docker Installation](https://docs.docker.com/engine/install/ubuntu/)


<h4><strong>Group Member Contributions</strong></h4><br>
Elizabeth Elias wrote a majority of the inital code for this project which was subsequently built on by her additional group members to add more specific functionality. 
Elizabeth was chiefly responsible for developing the web scraper and deciding which software to use for the project and produced a functional web scraper that returned 
the necessary information for our target websites and converting it into a human-readable format using an NLP tool known as HtmlToPlaintext which required a familiarity with Docker as well. Following the completion of the web scraper, the other group members cleaned the human readable data into a structure that was more favorable for data analysis, to which Elizabeth was the primary group member that developed the visualizations and ran the analysis on the final cleaned data. 


Data:<br>
<ul>
<li> DNSMPI_Files (gives all the DSNMPI files for the websites) and html_policies (gives all the html_policies) are under data folder in A5 and give the data we scraped from the websites privacy policies information.
<li>csvData.csv is a running csv file that updates after each crawler.py call with all the information scraped from our crawler.py.
<li> FinalTableData.csv is a final csv file that we ran from our crawler that we based all out statistics and analysis off of.
<ul>
<li> It sorts all the information into eight categories, titled: Website,Number of Pages,Number of Cookies,Contains DNSMPI-associated Content?,DNSMPI Content,Cookie Information,HTTP/HTTPS Policies Category,Mixed Content
</ul>

</ul>

<h4><strong>Credit Reel:</strong></h4> <br>
<ul>
<li> - Resources listed above -
<li> - Assigned readings from class - 
<li>[Analysis Paper Context Information](https://www.pewresearch.org/short-reads/2023/11/22/online-shopping-has-grown-rapidly-in-u-s-but-most-sales-are-still-in-stores/)
<li>[Data Modeling](https://www.w3schools.com/python/matplotlib_pyplot.asp)
</ul>
