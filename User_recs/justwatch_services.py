import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from tqdm import tqdm

def getSoupPlaywright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        browser.close()
        return BeautifulSoup(content, 'html.parser')

jw_urls = pd.read_csv('jw_soup_urls.csv')
jw_urls = jw_urls['url'].tolist()

url = jw_urls[0]
print(url)
soup = getSoupPlaywright(url)
us_url = soup.find(attrs={"hreflang": "en-US"})['href']
print(us_url)

us_urls = []

for url in tqdm(jw_urls):
    soup = getSoupPlaywright(url)
    us_urls.append(soup.find(attrs={"hreflang": "en-US"})['href'])