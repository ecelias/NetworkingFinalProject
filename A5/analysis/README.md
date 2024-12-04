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
<li>scipy
<li>adjustText
<li> ast
</ul>

Make the following directories inside HtmlToPlaintext: <code>./ext/html_policies</code> and <code>./ext/plaintext_policies</code> <br><br>
Install and run docker with the [setup guide](https://docs.docker.com/engine/install/ubuntu/) 

<h5>Running HtmlToPlaintext</h5>
Ensure all html files are located in <code>cd ~/HtmlToPlaintext/ext/html_policies</code> <br><br>
In the terminal, navigate to <code>cd ~/HtmlToPlaintext</code>. <br><br>
In the terminal run, <code>sudo ./build.sh </code><br><br>
In the terminal run, <code>sudo ./run.sh </code><br><br>
All HTML files should now be located in <code>./ext/plaintext_policies</code> as plaintext files.


<h5> Run createGraphs:</h5>
<ul>
<li> Make sure you installed all  libraries above, by doing pip install {library}
<li> Then run the code in the command line <code> python3 analysis/createGraphs.py </code>
<li> Graphs should then appear under ImageFiles 
</ul>

<h5> Data Description:</h5>
<ul>
<li>The CreateGraphs.py devloped the graphs that visualized the results of our web scarper 
<li>The HtmlToPlaintext/ext/html_policies gives all the html files of each website outputed from our crawler.py code
<li> The cookie_summary_data states all the cookie information that we had gotten from each website 
<li> The privacy_policy_data.json gives all the privacy policy data collected from the websites privavcy policy pages, sorted by website 
<li> The summary_statistics, implemented in the createGraphs.py, states some of the statistics that we had gathered from the data 
</ul> 

<h5> Credit Reel </h5>
<ul>
<li>Madeline Harbaugh (mharbaugh) contributions:<br>
<ul>
<li>Wrote code for num_dnsmpi_links(),percent_websites_per_category_with_dnsmpi_links(),percent_http_only_cookies_by_category(), percent_cookies_that_do_not_expire_by_category()
</ul>


<li>Kristin To (kto) contributions:<br>
<ul>
<li> Wrote code for pages_per_website(), cookies_per_website(), avg_pages_cookies_by_category(), pages_cookies_by_category(), and get_cookie_details(),
</ul>


<li>Elizabeth Elias (ecelias) contributions:<br>
<ul> 
<li> Wrote code for the cookies_with_http_only_tf(), cookies_to_dnsmpi_links(), cookies_all_websites(), cookie_domains_all_websites(), cookie_datatable(), summary_statistics(), correlation_matrix(column1, column2), and calc_num_appearances_by_cat(cookie_name, websites, sites_with_cookie)
<li> Wrote the data desceription, the credit reel, and the resources part of the analysis/README.md
</ul>


<li>Maria Gauna (mgauna) contributions:<br>
<ul>
<li>Wrote code for mixed_content(), protocol_content(), and percent_secure_cookies_by_category(), 
<li> Wrote the beginning part of the analysis/README.md
</ul>
</ul>

<h5>Resources</h5>
<ul>
<li>[HtmlToPlaintext](https://github.com/benandow/HtmlToPlaintext)
<li>[Docker Installation](https://docs.docker.com/engine/install/ubuntu/)
<li>
</ul>