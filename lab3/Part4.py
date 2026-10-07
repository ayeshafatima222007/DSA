import re
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("https://www.flipkart.com/search?q=gaming%20laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")

time.sleep(5)   # wait for the page to load

soup = BeautifulSoup(driver.page_source, 'html.parser')

products = []   # list to store name of the product
prices = []     # list to store price of the product
ratings = []    # list to store rating of the product

for card in soup.find_all('div', attrs={'data-id': True}):
    texts = list(card.stripped_strings)

    name = ''
    price = ''
    rating = ''

    for text in texts:
        if text == 'Add to Compare':
            continue
        if name == '':
            name = text                              # first text = product name
        if re.fullmatch(r'\d\.\d', text) and rating == '':
            rating = text                            # looks like 4.3
        if text.startswith('₹') and price == '':
            price = text                             # first price shown

    products.append(name)
    prices.append(price)
    ratings.append(rating)

driver.quit()

df = pd.DataFrame({'Product Name': products, 'Price': prices, 'Rating': ratings})
df.to_csv('products.csv', index=False, encoding='utf-8')

print(df)
print('Total products saved:', len(df))