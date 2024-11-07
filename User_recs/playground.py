from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import csv

def getIntfromStr(text) -> int:
    indxs = [i for i in range(len(text)) if text[i].isdigit()]
    res = int(''.join([text[i] for i in indxs]))
    return res

def load_all_items(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto(url)
        page.goto(url)
        val = BeautifulSoup(page.content(), 'html.parser').find('div', class_='titles-count').text
        val = getIntfromStr(val)
        print(val)
        prev_height = page.evaluate("document.body.scrollHeight")

        while True:
            time.sleep(1)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == prev_height:
                break
            prev_height = new_height
            print('+40')


        content = page.content()
        browser.close()
        return content  


url = 'https://www.justwatch.com/es/proveedor/max/peliculas?page=4'
jwurl = 'https://www.justwatch.com'

content = load_all_items(url)

soup = BeautifulSoup(content, 'html.parser')
soup_urls = soup.find_all('a', class_='title-list-grid__item--link')

urls = []

for i in soup_urls:
    urls.append(i['href'])

urls = [[jwurl+i] for i in urls]
print(urls)

with open('jw_soup_urls.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(['url'])
    wr.writerows(urls)

# movie_names = []
# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()

#     for url in urls:
#         page.goto(url)
#         us_url = BeautifulSoup(page.content(), 'html.parser').find('link', hreflang_='en-US')['href']
#         print(us_url, us_url.rfind('/'), us_url[us_url.rfind('/'):])
    
#     browser.close()



