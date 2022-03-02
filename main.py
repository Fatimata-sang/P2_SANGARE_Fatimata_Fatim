# Python programme pour scrape books.toscrape.com
# Et enregistrer les informations
import requests
from bs4 import BeautifulSoup
import csv
from function import extract_value
from urllib.parse import urljoin

# requests et scraping avec BeautifulSoup
url = "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"

response = requests.get(url)  # requeter le contenu de la page
soup = BeautifulSoup(response.content, 'html.parser')  # scraper les donnees
footer_element = soup.select_one('li.current')
cols = []  # liste pour enregistrer les infos

# recuperer un produit avec pagination ou non
if footer_element:
    while True:
        response2 = requests.get(url)
        soup2 = BeautifulSoup(response2.content, 'html.parser')

        footer_element = soup2.select_one('li.current')

        # pagination
        # trouver la page suivante à scraper
        next_page_element = soup2.select_one('li.next > a')
        if next_page_element:
            next_page_url = next_page_element.get('href')
            url = urljoin(url, next_page_url)
            produits = soup2.find_all('div', attrs={"class": "image_container"})
            for produit in produits:
                # requete pour scraper chaque produit
                id_produit = produit.find('a', href=True)['href'].split("/")[3]
                url2 = "http://books.toscrape.com/catalogue/" + id_produit + "/index.html"
                response3 = requests.get(url2)  # requeter le contenu de la page
                soup3 = BeautifulSoup(response3.content, 'html.parser')  # scraper les donnees

                # extraction des informations
                table = soup3.find('table')
                col_table = extract_value(table)
                col_table['category'] = soup3.find('ul', attrs={"class": "breadcrumb"}).find_all('li')[2].text
                col_table['description'] = soup3.select_one('div#product_description ~ p').text.strip()
                col_table['title'] = soup3.title.text.strip()
                col_table['image_url'] = soup3.find('img')['src'].replace("../../", "http://books.toscrape.com/")
                col_table['product_page_url'] = url2
                cols.append(col_table)
        else:
            break

else:
    produits = soup.find_all('div', attrs={"class": "image_container"})
    for produit in produits:
        # requete pour scraper chaque produit
        id_produit = produit.find('a', href=True)['href'].split("/")[3]
        url2 = "http://books.toscrape.com/catalogue/" + id_produit + "/index.html"
        response2 = requests.get(url2)  # requeter le contenu de la page
        soup2 = BeautifulSoup(response2.content, 'html.parser')  # scraper les donnees

        # extraction des informations
        table = soup2.find('table')
        col_table = extract_value(table)
        col_table['category'] = soup2.find('ul', attrs={"class": "breadcrumb"}).find_all('li')[2].text
        col_table['description'] = soup2.select_one('div#product_description ~ p').text.strip()
        col_table['title'] = soup2.title.text.strip()
        col_table['image_url'] = soup2.find('img')['src'].replace("../../", "http://books.toscrape.com/")
        col_table['product_page_url'] = url2
        cols.append(col_table)

# Enregistrement dans un fichier CSV
filename = 'categorie.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, ['product_page_url', 'universal_ product_code', 'price_including_tax', 'price_excluding_tax',
                           'number_available',
                           'review_rating', 'category', 'description', 'title', 'image_url'])
    w.writeheader()
    for col in cols:
        w.writerow(col)