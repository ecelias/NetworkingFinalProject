from bs4 import BeautifulSoup
import requests
from html.parser import HTMLParser
import asyncio
import json
from playwright.sync_api import sync_playwright
import csv
import matplotlib.pyplot as plt


USER_HEADERS = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
EXTRA_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"          
}

# scrape a website and return the html contents of the page
def scrape_hyperlinks(url):
    try:
        with sync_playwright() as p:
            browser = p.firefox.launch()
            context = browser.new_context(user_agent=USER_HEADERS, extra_http_headers=EXTRA_HEADERS)
            page = context.new_page()
            page.goto(url, timeout=600000)
            html_content = page.content()
            # Retrieve cookies and save to a string
            cookies = context.cookies()
            cookie_num = len(cookies)
            cookie_data = [f"Number of cookies collected: {len(cookies)}"]
            for cookie in cookies:
                cookie_data.append({
                    "Name": cookie.get("name"),
                    "Value": cookie.get("value"),
                    "Domain": cookie.get("domain"),
                    "Path": cookie.get("path"),
                    "Expires": cookie.get("expires"),
                    "Secure": cookie.get("secure"),
                    "HttpOnly": cookie.get("httpOnly")
                })
            browser.close()
            return html_content, cookie_data, cookie_num
    except TimeoutError:
        print(f"Timeout occurred for {url} after {600000 / 1000} seconds.")
        return None
    except Exception as e:
        print(f"An error occurred for {url}: {e}")
        return None

# inspect 
def inspect_homepage_html(html_file):
    hyperlinks = []
    soup = BeautifulSoup(html_file, 'html.parser')
    link_num = 1

    # find all the anchor tags with "href"
    for link in soup.find_all('a', href=True):
        current_link = link['href']

        data_analytics = link.get('data-analytics-title')
        data_aa = link.get('data-aa-analytics')
        category = data_analytics if data_analytics else data_aa

        privacy_terms = ["privacy", "cookie", "terms", "user agreement", 
                    "service agreement", "conditions of use", "terms of usage",
                    "privacy notice", "privacy policy", "privacy cookies"]

        if category:
            link_data = {category: current_link}
            hyperlinks.append(link_data)
        elif any(term.lower() in current_link.lower() for term in privacy_terms):
            # link not contained to specific category
            # setting to homepage + index keeps unique title in dictionary
            link_data = {f"homepage{link_num}": current_link}
            link_num += 1
            hyperlinks.append(link_data)
    #print(hyperlinks)
    return hyperlinks

def filter_for_privacy_page(hyperlink_dictionary):
    privacy_pages = {}
    num_dnsmpi_links = {}
    dnsmpi_links = {}

    privacy_terms = ["privacy", "cookie", "terms", "user agreement", 
                    "service agreement", "conditions of use", "terms of usage",
                    "privacy notice", "privacy policy", "privacy cookies", "ccpa", "dnsmpi", 
                    "do not sell my personal information", "do not sell my information", 
                    "do not sell my info", "do not sell my personal info", "do not sell or share my personal information", 
                    "do not sell / share my personal information", "do not sell/share my personal information",
                    "do not sell or share my information", "do not sell or share my info", 
                    "do not sell or share my personal info", "California Consumer Privacy Act", 
                    "Your California privacy rights","CCPA rights","California privacy disclosures", "Do not share my data",
                    "California opt-out"]
    
    dnsmpi_terms = ["ccpa", "dnsmpi", "do not sell my personal information", "do not sell my information", 
                    "do not sell my info", "do not sell my personal info", "do not sell or share my personal information",
                    "do not sell / share my personal information", "do not sell/share my personal information", 
                    "do not sell or share my information", "do not sell or share my info", 
                    "do not sell or share my personal info", "California Consumer Privacy Act", 
                    "Your California privacy rights","CCPA rights","California privacy disclosures", "Do not share my data",
                    "California opt-out"]

    for url, categories in hyperlink_dictionary.items():
        hyperlinks = []
        dnsmpi_hyperlinks = []
        num_dnsmpi_hyperlinks = 0
        for category in categories:
            for key, value in category.items():
                if any(term.lower() in key.lower() or term.lower() in value.lower() for term in privacy_terms):
                    hyperlinks.append(category)
                if any(term.lower() in key.lower() or term.lower() in value.lower() for term in dnsmpi_terms):
                    dnsmpi_hyperlinks.append(category)
                    num_dnsmpi_hyperlinks += 1
        privacy_pages[url] = hyperlinks   
        num_dnsmpi_links[url] = num_dnsmpi_hyperlinks
        dnsmpi_links[url] = dnsmpi_hyperlinks
    return privacy_pages, dnsmpi_links, num_dnsmpi_links


def scrape_homepages_for_privacy_policy_pages(filename):
    hyperlinks_in_url = {}
    privacy_page_hyperlinks = {}
    file = open(filename, 'r+')
    for line_number, link in enumerate(file, start=1):
        link = link.strip()
        html_content = scrape_hyperlinks(link)
        hyperlinks_in_url[link] = inspect_homepage_html(html_content)
    privacy_pages = filter_for_privacy_page(hyperlinks_in_url)  
    return privacy_page_hyperlinks


def scrape_for_priv_policy(homepage, policypage, current_policy_page):
    page_name = homepage + policypage
    if "http" in policypage:
        page_name = policypage
    try:
        with sync_playwright() as p:
            browser = p.firefox.launch()
            context = browser.new_context(user_agent=USER_HEADERS, extra_http_headers=EXTRA_HEADERS)
            page = context.new_page()
            page.goto(page_name, timeout=300000)
            html_content = page.content()
            browser.close()
            html_file_name = "analysis/HtmlToPlaintext/ext/html_policies/" + homepage.split(".")[1] + "_" + str(current_policy_page) +".html"
            html_file_name2 = "data/html_policies/" + homepage.split(".")[1] + "_" + str(current_policy_page) +".html"
            with open(html_file_name, "w") as f:
                f.write(html_content)
            with open(html_file_name2, "w") as f2:
                f2.write(html_content)
            return page_name, html_content
    except TimeoutError:
        print(f"Timeout occurred for {page_name} after {300000 / 1000} seconds.")
        return None
    except Exception as e:
        print(f"An error occurred for {page_name}: {e}")
        return None


def inspect_privacy_policy_html(html_file):
    content = {}
    soup = BeautifulSoup(html_file, 'html.parser')
    no_anchor_num = 0;

    # find all the anchor tags with "href"
    for chunk in soup.find_all('p'):
        current_anchor = chunk.get('id')
        current_text = chunk.get_text(strip=True)

        if current_anchor:
            anchor_name = current_anchor
        else: 
            anchor_name = "no_anchor" + str(no_anchor_num)
            no_anchor_num +=1

        content[anchor_name] = current_text
    
    return content

def check_mixed_content(link):
    #Checks if link is a HTTPS link
    if not link.startswith("https://"):
        return "Not applicable"

    #Gets the HTML of the page 
    try: 
        try:
            response = requests.get(link, timeout = 10)
            response.raise_for_status
        except requests.ConnectionError:
            return "Denied"
    except requests.RequestException as e:
        print(f'Error fetching {link}:{e}')
        return "Denied"

    soup = BeautifulSoup(response.text, "html.parser")

    #Find all resource links
    resources = []
    for tag in soup.find_all(['img','script','link']):
        src = tag.get('src') or tag.get('href')
        if src:
            resources.append(src)
    
    #Checks if the links are loaded over HTTP
    mixed_content_found = False
    for resource in resources:
        if resource.startswith("http://"):
            resource_url = resource 
        elif resource.startswith("/"):
            continue
        else:
            continue
        #Checks if the resource if loaded over HTTP    
        if resource_url.startswith("http://"):
            mixed_content_found = True

    #Returns result if the page is mixed content
    if mixed_content_found:
        return "True"
    else:
        return "False"

def check_policites(link):
    result = {"https": False, "http": False}

    https_link = link.replace("http://", "https://")
    try:
        response_https = requests.get(https_link, timeout = 10)
        if (299 >= response_https.status_code) and (response_https.status_code >= 200):
            result["https"] = True
    except requests.RequestException:
        pass
    
    http_link= link.replace("https://", "http://")
    try:
        try:
            response_http = requests.get(http_link, timeout = 10)
        except requests.ConnectionError:
            print("Connection failed.")
        if (299 >= response_http.status_code) and (response_http.status_code >= 200):
            result["http"] = True
    except requests.RequestException:
        pass        
    
    if result["http"] and result["https"]:
        return "both"
    elif result["https"]:
        return "HTTPS-Only"
    elif result["http"]:
        return "HTTP-Only"
    else:
        return "Neither"
               
    
    
def main():
    file = open('raw_website_links.txt', 'r+')
    csvResults = []
    websites = []
    number_of_pages = []
    number_of_cookies = []
    for line_number, link in enumerate(file, start=1):
        hyperlinks_in_url = {}
        privacy_page_hyperlinks = {}
        link = link.strip()
        mixed_results = check_mixed_content(link)
        policies_result = check_policites(link)

        result = scrape_hyperlinks(link)
        if result is not None:
            html_content, cookie_string, cookie_num = result
            hyperlinks_in_url[link] = inspect_homepage_html(html_content)

            privacy_page_urls, dnsmpi_links, num_dnsmpi_links = filter_for_privacy_page(hyperlinks_in_url)  
            privacy_policy_content = {}

            for website, priv_policy_pages in privacy_page_urls.items():
                dnsmpi_content = []
                current_page_index = 0;
                for page_info in priv_policy_pages:
                    for category, priv_policy_page in page_info.items():
                        priv_page_info = scrape_for_priv_policy(website, priv_policy_page, current_page_index)
                        if priv_page_info is not None:
                            pol_content = inspect_privacy_policy_html(priv_page_info[1])
                            privacy_policy_content[website + ", " + priv_page_info[0]] = pol_content
                            current_page_index += 1
                            testFile.write(f"{current_page_index}\n")
                            if priv_policy_page in dnsmpi_links.get(website):
                                dnsmpi_content.append(pol_content)

                nDNSMPI = num_dnsmpi_links[website]
                if nDNSMPI > 0:
                    has_dnsmpi = "Yes"
                else:
                    has_dnsmpi = "No"

                csvResults.append([website, current_page_index, cookie_num, has_dnsmpi, dnsmpi_content, cookie_string, policies_result, mixed_results])
                websites.append(website)
                number_of_pages.append(current_page_index)
                number_of_cookies.append(cookie_num)

            json_filename = "analysis/privacy_policy_data.json"
            # Dump the dictionary to a JSON file
            with open(json_filename, 'a') as json_file:
                json.dump(privacy_policy_content, json_file, indent=4)  # Use indent for pretty formatting

    if csvResults:
        with open("data/csvData.csv", "a", newline="") as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Check if file is empty to write the header row only once
                writer.writerow(["Website", "Number of Pages", "Number of Cookies", "Contains DNSMPI-associated Content?", "DNSMPI Content", "Cookie Information", "HTTP/HTTPS Policies Category", "Mixed Content"])
            writer.writerows(csvResults)
    else:
        print("No results to write to the CSV file.")

if __name__ == "__main__":
    main()


    
    