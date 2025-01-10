from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

app = Flask(__name__)

def get_lowest_price_product(brand):
    s = Service('/opt/homebrew/bin/chromedriver')
    options = webdriver.ChromeOptions()
    options.headless = True  # Run Chrome in headless mode
    driver = webdriver.Chrome(service=s, options=options)
    url = f"https://www.ebay.com/sch/i.html?_nkw={brand.replace(' ', '+')}&_sop=15"
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.s-item__title')))
    time.sleep(3)

    products = driver.find_elements(By.CSS_SELECTOR, '.s-item__wrapper')
    lowest_price = float('inf')
    lowest_price_product = None

    for product in products:
        price_text = product.find_element(By.CSS_SELECTOR, '.s-item__price').text
        match = re.search(r'\d+[\.,]?\d*', price_text.replace('US $', '').replace(',', ''))
        if match:
            price = float(match.group().replace(',', ''))
            title = product.find_element(By.CSS_SELECTOR, '.s-item__title').text
            if price < lowest_price:
                lowest_price = price
                lowest_price_product = title

    driver.quit()
    return lowest_price_product, lowest_price

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/compare', methods=['POST'])
def compare():
    brand1 = request.form['brand1']
    brand2 = request.form['brand2']
    product1, price1 = get_lowest_price_product(brand1)
    product2, price2 = get_lowest_price_product(brand2)
    # Compare the two prices to determine the overall lowest price
    overall_lowest = min(price1, price2)
    if overall_lowest == price1:
        result = f'Overall lowest priced product is {product1} from {brand1}, priced at US ${price1}'
    else:
        result = f'Overall lowest priced product is {product2} from {brand2}, priced at US ${price2}'

    return f'''
        <h1>Results</h1>
        <p>Lowest priced {brand1} product: {product1}, priced at US ${price1}</p>
        <p>Lowest priced {brand2} product: {product2}, priced at US ${price2}</p>
        <p>{result}</p>
        <a href="/">Back</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)