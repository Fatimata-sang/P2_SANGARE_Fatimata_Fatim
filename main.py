# Python programme pour scrape books.toscrape.com
# Et enregistrer les informations
import requests
from bs4 import BeautifulSoup
import csv
from function import *

# requests et scraping avec BeautifulSoup
URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(URL) # requeter le contenu de la page
soup = BeautifulSoup(page.content, 'html.parser') # scraper les donnees

cols = []  # liste pour enregistrer les infos

# extraction des informations
table = soup.find('table')
col_table = extract_value(table)
col_table['category'] = soup.find('ul', attrs={"class": "breadcrumb"}).find_all('li')[2].text
col_table['description'] = soup.select_one('div#product_description ~ p').text.strip()
col_table['title'] = soup.title.text.strip()
col_table['image_url'] = soup.find('img')['src']
col_table['product_page_url'] = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
cols.append(col_table)

# Enregistrement dans un fichier CSV
filename = 'inspirational_quotes3.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, ['product_page_url', 'universal_ product_code', 'price_including_tax', 'price_excluding_tax', 'number_available',
                           'review_rating', 'category', 'description', 'title', 'image_url'])
    w.writeheader()
    for col in cols:
        w.writerow(col)