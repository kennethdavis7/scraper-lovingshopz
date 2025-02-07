import pandas as pd
from pandas import read_csv
import os
import requests
import time

# products = read_csv("/Users/kennethdavis/Documents/scrape_lovingshopz/raw_csv/products.csv")
# images = read_csv("/Users/kennethdavis/Documents/scrape_lovingshopz/raw_csv/image_products.csv")

# products['qty'] = products['qty'].str.replace('Sisa ', '')
# products['qty'] = products['qty'].str.replace(r',\s*\d+\s*rb', '000', regex=True)
# products['qty'] = products['qty'].str.replace(' rb', '000')
# products['qty'] = products['qty'].str.replace('.', '')


# for x in products.index:
#     if products.loc[x, 'qty'] == 'Habis' or products.loc[x, 'qty'] == 'Tidak Dijual':
#         products.drop(x, inplace=True)
#         for n in images.index:
#             if images.loc[n, 'product_id'] == x + 1:
#                 images.drop(n, inplace=True)
                
# products.reset_index(drop=True, inplace=True)
# images.reset_index(drop=True, inplace=True)

# products.index = products.index + 1
# images.index = images.index + 1

# products.drop(columns="id", inplace=True)
# images.drop(columns="id", inplace=True)

# products.index.rename('id', inplace=True)
# images.index.rename('id', inplace=True)

# seen = {}
# count = 1
# for i in images.index:
#     if images.loc[i, 'product_id'] not in seen:
#         seen[images.loc[i, 'product_id']] = count
#         count+=1
#     images.loc[i, 'product_id'] = seen[images.loc[i, 'product_id']]
    
# for g in images.index:
#     images.loc[g, 'url'] = 'storage/' + 'images/' + str(g) + "-" + images.loc[g, 'alt'].replace(' ', '-').replace('/', '')
#     images.loc[g, 'alt'] = str(g) + "-" + images.loc[g, 'alt'].replace(' ', '-').replace('/', '')

# images.to_csv("/Users/kennethdavis/Documents/scrape_lovingshopz/clean_csv/clean_image_products.csv")
# products.to_csv("/Users/kennethdavis/Documents/scrape_lovingshopz/clean_csv/clean_products.csv")

# os.mkdir(os.path.join(os.getcwd(), 'images'))

# os.chdir(os.path.join(os.getcwd(), 'images'))

# for m in images.index:
#     print('Saving ' + str(m) + ' images')
#     with open(str(m) + "-" + images.loc[m, 'alt'].replace(' ', '-').replace('/', ''), 'wb') as f:
#         im = requests.get(images.loc[m, 'url'])
#         f.write(im.content)
products = pd.read_csv("/Users/kennethdavis/Documents/scrape_lovingshopz/clean_csv/clean_products_copy.csv")  
products.insert(8, column = "click", value = 0)  

products.to_csv("/Users/kennethdavis/Documents/scrape_lovingshopz/clean_csv/clean_products_revision.csv", index=False)
    




