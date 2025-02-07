from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import os

opts = Options()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/537.36 (KHTML, like Gecko) Version/12.0.17 Safari/627.1"
opts.add_argument("user-agent=" + user_agent)
opts.add_argument("--headless")

service = Service(executable_path="/Users/kennethdavis/Documents/scrape_lovingshopz/chromedriver")

driver = webdriver.Chrome(options=opts, service=service)
check_user_agent = driver.execute_script("return navigator.userAgent")

driver.get('https://www.tokopedia.com/lovingshopz/product')

driver.execute_script("""
    var iframe = document.querySelector('iframe[src^="https://accounts.google.com/gsi/iframe"]');
    if (iframe) {
        iframe.parentElement.removeChild(iframe);
    }
""")

driver.maximize_window()

soup = BeautifulSoup(driver.page_source, 'html.parser')

categories_html = soup.find_all('li', class_="css-1239vz0")

base_url = 'https://www.tokopedia.com'

current_timestamp = datetime.now()
formatted_timestamp = current_timestamp.strftime('%Y-%m-%d %H:%M:%S')

categories = []
category_hrefs = []
for index, category in enumerate(categories_html[3:]):
    a = category.find('a', href=True)
    href = base_url + a['href']
    name_category = a.text
    
    categories.append({
        'id': index + 1,
        'name': name_category,
        'status': 1,
        'created_at': formatted_timestamp,
        'updated_at': formatted_timestamp,
    })
    
    category_hrefs.append(href)

product_id = 1196
image_id = 5310
category_id = 50
for category_href in category_hrefs[49:]:
    for i in range(20):
        driver.get(category_href + '/page/' + str(i + 1))
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(2)
        empty_products = soup.find('h5', 'css-1x8eu1x-unf-heading e1qvo2ff5')
        
        if empty_products is None:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#zeus-root')))
            time.sleep(2)
            
            print('Scanning...')
            for i in range(17):
                driver.execute_script('window.scrollBy(0, 250)')
                time.sleep(2)


            soup = BeautifulSoup(driver.page_source, "html.parser")

            product_links = [] 
            for product in soup.find_all('div', class_='prd_container-card css-126fhq2'):
                for link in product.find_all('a', class_='pcv3__info-content css-gwkf0u',href=True):
                    product_links.append(link['href'])
            
            for index, link in enumerate(product_links):
                driver.get(link)
                
                products = []
                image_products = []

                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#zeus-root')))
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-testid="lblPDPDescriptionProduk"]')))
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'p[data-testid="stock-label"]')))
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.css-1os9jjn')))
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.price')))
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul[data-testid="lblPDPInfoProduk"]')))


                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                product_title = soup.find("h1", class_="css-1os9jjn").text.strip()
                
                print('Saving: ' + product_title)

                product_description = soup.find('div', {'data-testid': 'lblPDPDescriptionProduk'}).contents
                product_description = ''.join(str(item) for item in product_description)
                    
                product_stock = soup.find('p', class_='css-1yy88m3-unf-heading e1qvo2ff8').find('b').text.strip()

                product_price = int(soup.find('div', class_="price").text.replace('Rp', '').replace('.', ''))

                min_order_li = soup.find_all('li', class_="css-bwcbiv")[1]
                min_order = int(min_order_li.find('span', class_="main").text.strip().split(' ')[0])

                buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-testid="PDPImageThumbnail"]')

                previous_image_src = None
                for index, button in enumerate(buttons):
                    if index >= 4:
                        try:
                            slide_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="btnPDPImageSliderNext"]')
                            action = ActionChains(driver)
                            action.move_to_element(slide_button).perform()
                            slide_button.click()
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="PDPImageThumbnail"]')))
                            time.sleep(10)
                        except:
                            pass
                    
                    button.click()
                    
                    time.sleep(5)
                    
                    # Fetch the current page source
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    # Find the image element for the current product image
                    product_img = soup.find('img', class_='css-1c345mg', src=True)
                    
                    # Extract image source and alt text
                    image_src = product_img['src']
                    image_alt = product_img['alt']
                    
                    # Check if the image source has changed
                    if image_src != previous_image_src:
                        image_products.append({
                            'id': image_id, # continue
                            'product_id': product_id,
                            'url': image_src,
                            'alt' : image_alt.replace(' ', '-').replace('/', '') + str(i) + '.jpg',
                            'created_at': formatted_timestamp,
                            'updated_at': formatted_timestamp,
                        })
                        image_id += 1
                    
                    # Update the previous image source
                    previous_image_src = image_src

                products.append({
                    'id': product_id,
                    'category_id': category_id,
                    'price': product_price,
                    'name': product_title,
                    'qty': product_stock,
                    'description': product_description,
                    'min_order': min_order,
                    'status': 1,
                    'created_at': formatted_timestamp,
                    'updated_at': formatted_timestamp,
                })
                
                df1 = pd.DataFrame(products)
                df2 = pd.DataFrame(image_products)
                # df3 = pd.DataFrame(categories)
                
                df1.to_csv(r'/Users/kennethdavis/Documents/scrape_lovingshopz/csv/products.csv', mode='a', header=False, index=False) 
                df2.to_csv(r'/Users/kennethdavis/Documents/scrape_lovingshopz/csv/image_products.csv', mode='a', header=False, index=False) 
                # df3.to_csv(r'/Users/kennethdavis/Documents/scrape_lovingshopz/csv/categories.csv', index=False)
                
                # mode='a', header=False (add this for continuing)
                # and this [category_id:]
                
                print('Saved: ' + product_title)
                product_id += 1
        else:
            category_id += 1
            break

time.sleep(600)
