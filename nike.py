from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re  # Importing the regex library

# Specify the path to ChromeDriver
s = Service('/opt/homebrew/bin/chromedriver')  # Update this path to your chromedriver location

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

# Create a Chrome driver using the Service object
driver = webdriver.Chrome(service=s, options=options)

def get_lowest_price_product(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.s-item__title')))
    time.sleep(3)  # Wait additional time to ensure JavaScript scripts are fully executed

    products = driver.find_elements(By.CSS_SELECTOR, '.s-item__wrapper')
    lowest_price = float('inf')
    lowest_price_product = None

    for product in products:
        price_text = product.find_element(By.CSS_SELECTOR, '.s-item__price').text
        # Extract the numeric part of the price using regex
        match = re.search(r'\d+[\.,]?\d*', price_text.replace('US $', '').replace(',', ''))
        if match:
            price = float(match.group().replace(',', ''))
            title = product.find_element(By.CSS_SELECTOR, '.s-item__title').text
            if price < lowest_price:
                lowest_price = price
                lowest_price_product = title
        else:
            print(f"Unable to extract price: {price_text}")

    return lowest_price_product, lowest_price  # Return the product and the price

url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=nike&_sacat=0&_odkw=nike&_osacat=0'
product, price = get_lowest_price_product(url)
if product:
    print(f"The lowest priced product is: {product}, priced at: US ${price}")
else:
    print("Unable to retrieve valid product pricing information.")

driver.quit()