from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return webdriver.Chrome(options=options)

def get_page_content(url, driver):
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-id]")))
    return driver.page_source

def extract_product_info(product):
    name = product.select_one('div.KzDlHZ')
    price = product.select_one('div.Nx9bqj')
    image = product.select_one('img.DByuf4')
    link = product.select_one('a.CGtC98')
    
    if all([name, image, link]):
        return {
            'name': name.text.strip(),
            'price': price.text.strip() if price else "Currently unavailable",
            'image_url': image.get('src', ''),
            'product_url': 'https://www.flipkart.com' + link.get('href', '')
        }
    return None

def scrape_multiple_flipkart_products(keyword, num_products=3):
    url = f"https://www.flipkart.com/search?q={keyword.replace(' ', '+')}"
    driver = setup_driver()
    
    try:
        page_content = get_page_content(url, driver)
        soup = BeautifulSoup(page_content, 'html.parser')
        product_divs = soup.select('div[data-id]')
        
        products = []
        for product_div in product_divs:
            if len(products) >= num_products:
                break
            product = extract_product_info(product_div)
            if product:
                products.append(product)
        
        logger.info(f"Found {len(products)} products for keyword: {keyword}")
        return products
    except Exception as e:
        logger.error(f"Error scraping Flipkart: {str(e)}")
        return []
    finally:
        driver.quit()

def main():
    keyword = input("Enter the product name to search on Flipkart: ")
    products = scrape_multiple_flipkart_products(keyword)
    
    if products:
        print(f"Found {len(products)} products:")
        for i, product in enumerate(products, 1):
            print(f"\nProduct {i}:")
            print(f"  Name: {product['name']}")
            print(f"  Price: {product['price']}")
            print(f"  Image URL: {product['image_url']}")
            print(f"  Product URL: {product['product_url']}")
    else:
        print(f"No products found for '{keyword}'")

if __name__ == "__main__":
    main()