# function.py
import re


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
            # elif re.search(r"Product Type", tr.find('th').text):
            #    target = tr.find('td')
            #    col_val['category'] = str(target.text.strip())
        except:
            return "Nothing_found"
    return col_val
