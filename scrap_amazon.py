import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_html_content_selenium(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={UserAgent().random}")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        return driver.page_source
    finally:
        driver.quit()

def extract_amazon_products(html_content, product_name):
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []
    
    def extract_product(element):
        name_elem = element.find(['span', 'h2'], class_=['a-size-medium a-color-base a-text-normal', 'a-size-mini a-spacing-none a-color-base s-line-clamp-2'])
        price_elem = element.find('span', class_=['a-price-whole'])
        image_elem = element.find('img', class_=['s-image', 'a-dynamic-image'])
        link_elem = element.find('a', class_=['a-link-normal s-no-outline', 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'])
        
        if name_elem and price_elem and image_elem and link_elem:
            return {
                'name': name_elem.text.strip(),
                'price': price_elem.text.strip().replace('₹', '').replace(',', ''),
                'image_url': image_elem.get('src', ''),
                'product_url': 'https://www.amazon.in' + link_elem.get('href', '')
            }
        return None

    keywords = set(product_name.lower().split())
    
    for div in soup.find_all('div', class_=['s-result-item', 'sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20', 'a-section a-spacing-base']):
        product = extract_product(div)
        if product:
            product_words = set(product['name'].lower().split())
            if keywords.intersection(product_words):
                products.append(product)

    # Sort products by relevance (number of matching keywords)
    sorted_products = sorted(products, key=lambda x: len(keywords.intersection(set(x['name'].lower().split()))), reverse=True)

    return sorted_products[:3]  # Return the top 3 most relevant products

def scrape_all(product_name):
    url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
    html_content = get_html_content_selenium(url)
    if html_content:
        return {'Amazon': extract_amazon_products(html_content, product_name)}
    return {'Amazon': []}

if __name__ == "__main__":
    product_name = input("Enter a product name to search: ")
    result = scrape_all(product_name)
    print("Product Details:")
    for marketplace, products in result.items():
        print(f"{marketplace}:")
        if products:
            for i, product in enumerate(products, 1):
                print(f"  Product {i}:")
                print(f"    Name: {product['name']}")
                print(f"    Price: ₹{product['price']}")
                print(f"    Image URL: {product['image_url']}")
                print(f"    Product URL: {product['product_url']}")
                print()
        else:
            print("  No relevant products found.")
        print()
    time.sleep(random.uniform(1, 3))