# function.py
import requests
from bs4 import BeautifulSoup
import re
import shutil
import os
import time
####################################
# extraction infos table function
####################################
def extract_value(balise):
    col_val = {}
    for tr in balise.find_all('tr'):
        try:
            if re.search(r"UPC", tr.find('th').text):
                target = tr.find('td')
                col_val['universal_ product_code'] = str(target.text.strip())
            elif re.search(r"incl. tax", tr.find('th').text):
                target = tr.find('td')
                col_val['price_including_tax'] = str(target.text.strip())
            elif re.search(r"excl. tax", tr.find('th').text):
                target = tr.find('td')
                col_val['price_excluding_tax'] = str(target.text.strip())
            elif re.search(r"Availability", tr.find('th').text):
                target = tr.find('td')
                col_val['number_available'] = re.findall('[0-9]+', str(target.text.strip()))[0]
            elif re.search(r"Number of reviews", tr.find('th').text):
                target = tr.find('td')
                col_val['review_rating'] = str(target.text.strip())
            elif re.search(r"Product Type", tr.find('th').text):
                target = tr.find('td')
                col_val['product_type'] = str(target.text.strip())
        except:
            return "Nothing_found"
    return col_val

def cut_string(stri, n):
    title_for_link = re.sub(r"[^A-Za-z0-9]+", "-", stri)  # remove all special character
    if len(stri) > n:
        short_title = title_for_link[0:n]  # cut after n character if it's too long
    else:
        short_title = title_for_link
    return short_title


def get_info(produits, url_base, images_folder):
    cols = []  # liste pour enregistrer les infos
    for produit in produits:
        time.sleep(1)  # assurer au moins 1 seconde entre les sraping de produit
        # requete pour scraper chaque produit
        id_produit = produit.find('a', href=True)['href'].split("/")[3]
        print("recuperation livre: ",id_produit)
        url = url_base + "catalogue/" + id_produit + "/index.html"
        response = requests.get(url, timeout=10)  # requeter le contenu de la page
        soup = BeautifulSoup(response.content, 'html.parser')  # scraper les donnees

        # extraction des informations
        table = soup.find('table')
        col_table = extract_value(table)
        col_table['category'] =soup.find('li', {'class': 'active'}).find_previous('a').text  #soup.find('ul', attrs={"class": "breadcrumb"}).find_all('li')[2].text
        col_table['description'] = str(soup.select_one('div#product_description ~ p')).replace('<p>', '').replace('</p>', '')
        col_table['title'] =soup.find("li", {"class": "active"}).text  #soup.title.text.strip()
        img_url = soup.find('img')['src'].replace("../../", url_base)
        img_name = soup.find('img')['alt'].strip()
        col_table['image_url'] = img_url
        col_table['product_page_url'] = url
        cols.append(col_table)
        r_img = requests.get(img_url, stream=True)  # Get request on full_url
        images_folder_link = images_folder
        if not os.path.exists(images_folder_link):
            os.mkdir(images_folder_link)
        nom_images = cut_string(img_name, 20)
        if r_img.status_code == 200:  # 200 status code = OK
            with open(images_folder_link + nom_images + '.jpg', 'wb') as f:
                r_img.raw.decode_content = True
                shutil.copyfileobj(r_img.raw, f)
    return cols