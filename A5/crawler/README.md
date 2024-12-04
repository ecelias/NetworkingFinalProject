<h2>Instructions for running <code>crawler.py</code></h2>

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
Navigate to the <code>cd ~/cs3640/A5</code> directory and <code>python3 crawler/crawler.py</code> in the terminal.

<h4><strong>Group Member Contributions</strong></h4><br>

Madeline Harbaugh (mharbaugh) contributions:<br>
<ul>
<li> Wrote code for scrape_hyperlinks(url) and inspect_homepage_html(html_file) methods
</ul>


Kristin To (kto) contributions:<br>
<ul>
<li> Wrote code for filter_for_privacy_page(hyperlink_dictionary) and the main() methods
</ul>


Elizabeth Elias (ecelias) contributions:<br>
<ul>
<li> Wrote code for inspect_privacy_policy_html(html_file), scrape_homepages_for_privacy_policy_pages(filename), and ndscrape_for_priv_policy(homepage, policypage, current_policy_page) methods
</ul>


Maria Gauna (mgauna) contributions:<br>
<ul>
<li> Wrote code for check_mixed_content(link) and check_policites(link) methods
<li> Wrote crawler/README.md file 
</ul>



<h4>Resources</h4>
<ul>
<li>[Using BeautifulSoup](https://oxylabs.io/blog/beautiful-soup-parsing-tutorial)
<li>[BeautifulSoup find_all method](https://scrapeops.io/python-web-scraping-playbook/python-beautifulsoup-findall/)
<li>[Using Playwright](https://www.roborabbit.com/blog/web-scraping-with-playwright-in-python/)
</ul>