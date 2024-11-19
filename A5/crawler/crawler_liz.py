from bs4 import BeautifulSoup
import requests
from html.parser import HTMLParser


def scrape_site(url):
    r = requests.get('https://www.temu.com')
    soup = BeautifulSoup(r.content, 'html.parser')


    hyperlinks = []
    # find all the anchor tags with "href"
    for link in soup.find_all('a'):
	    hyperlinks.append('href')