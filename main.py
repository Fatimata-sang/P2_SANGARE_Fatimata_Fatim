# Python programme pour scrape books.toscrape.com
# Et enregistrer les informations
import requests
from bs4 import BeautifulSoup
import csv
import os
from function import get_info
from urllib.parse import urljoin
import time

# création de dossiers
CSV_PATH = 'CSV/'
IMAGES_PATH = 'Images/'

if not os.path.exists(CSV_PATH):
    os.mkdir(CSV_PATH)
if not os.path.exists(IMAGES_PATH):
    os.mkdir(IMAGES_PATH)

# requests et scraping avec BeautifulSoup
url_base = "https://books.toscrape.com/"

response = requests.get(url_base, timeout=10)  # requeter le contenu de la page
soup = BeautifulSoup(response.content, 'html.parser')  # scraper les donnees
categories = soup.find('ul', attrs={"class": "nav nav-list"}).find('ul').find_all('li')


# recuperer les pages
for categorie in categories:
    url_categorie = url_base + categorie.find('a', href=True)['href']
    name_categorie = categorie.find('a').text.strip()
    response = requests.get(url_categorie, timeout=10)  # requeter le contenu de la page
    time.sleep(1) # assurer au moins 1 seconde entre les sraping de categories
    soup_categorie = BeautifulSoup(response.content, 'html.parser')  # scraper les donnees
    footer_element = soup_categorie.select_one('li.current')
    cols = []  # liste pour enregistrer les infos
    images_folder_link = IMAGES_PATH + name_categorie + '/'
    # recuperer un produit avec pagination ou non
    if footer_element:
        while True:
            response2 = requests.get(url_categorie, timeout=10)
            soup2 = BeautifulSoup(response2.content, 'html.parser')

            footer_element = soup2.select_one('li.current')

            # pagination
            # trouver la page suivante à scraper
            next_page_element = soup2.select_one('li.next > a')
            if next_page_element:
                next_page_url = next_page_element.get('href')
                url_categorie = urljoin(url_categorie, next_page_url)
                produits = soup2.find_all('div', attrs={"class": "image_container"}) # get all produit
                cols = get_info(produits, url_base, images_folder_link)
            else:
                break

    else:
        produits = soup_categorie.find_all('div', attrs={"class": "image_container"}) # get all produit
        cols = get_info(produits, url_base, images_folder_link) # get info

    # Enregistrement dans un fichier CSV
    filename = name_categorie + '.csv'
    with open(CSV_PATH + filename, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, ['product_page_url', 'universal_ product_code', 'price_including_tax', 'price_excluding_tax',
                               'number_available',
                               'review_rating', 'product_type', 'category', 'description', 'title', 'image_url'])
        w.writeheader()
        for col in cols:
            w.writerow(col)