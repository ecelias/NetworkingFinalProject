from bs4 import BeautifulSoup
import requests
from html.parser import HTMLParser
import asyncio
import json
from playwright.sync_api import sync_playwright

USER_HEADERS = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
EXTRA_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"          
}

# scrape a website and return the html contents of the page
def scrape_hyperlinks(url):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        context = browser.new_context(user_agent=USER_HEADERS, extra_http_headers=EXTRA_HEADERS)
        page = context.new_page()
        page.goto(url)
        html_content = page.content()
        browser.close()
        return html_content

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

    privacy_terms = ["privacy", "cookie", "terms", "user agreement", 
                    "service agreement", "conditions of use", "terms of usage",
                    "privacy notice", "privacy policy", "privacy cookies"]

    for url, categories in hyperlink_dictionary.items():
        hyperlinks = []
        for category in categories:
            for key, value in category.items():
                if any(term.lower() in key.lower() or term.lower() in value.lower() for term in privacy_terms):
                    hyperlinks.append(category)
        privacy_pages[url] = hyperlinks    
    return privacy_pages


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
    with sync_playwright() as p:
        browser = p.firefox.launch()
        context = browser.new_context(user_agent=USER_HEADERS, extra_http_headers=EXTRA_HEADERS)
        page = context.new_page()
        page.goto(page_name)
        html_content = page.content()
        browser.close()
        html_file_name = "data/" + homepage.split(".")[1] + "_" + str(current_policy_page) +".html"
        with open(html_file_name, "w") as f:
            f.write(html_content)
        return page_name, html_content


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


def main():
    hyperlinks_in_url = {}
    privacy_page_hyperlinks = {}
    file = open('example.txt', 'r+')
    for line_number, link in enumerate(file, start=1):
        link = link.strip()
        html_content = scrape_hyperlinks(link)
        hyperlinks_in_url[link] = inspect_homepage_html(html_content)

    privacy_page_urls = filter_for_privacy_page(hyperlinks_in_url)  
    privacy_policy_content = {}

    for website, priv_policy_pages in privacy_page_urls.items():
        for page_info in priv_policy_pages:
            current_page_index = 0;
            for category, priv_policy_page in page_info.items():
                page_name, priv_html_content = scrape_for_priv_policy(website, priv_policy_page, current_page_index)
                privacy_policy_content[website + ", " + page_name] = inspect_privacy_policy_html(priv_html_content)
                current_page_index += 1

    json_filename = f"privacy_policy_data.json"
    # Dump the dictionary to a JSON file
    with open(json_filename, 'w+') as json_file:
        json.dump(privacy_policy_content, json_file, indent=4)  # Use indent for pretty formatting

if __name__ == "__main__":
    main()


    
    