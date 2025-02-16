import json
import random
from scrap_amazon import scrape_all as scrape_amazon
from scrap_flipkart import scrape_multiple_flipkart_products
from scrap_gem import scrape_gem_products

def get_random_products(source, num_products=6):
    keywords = ["smartphone", "laptop", "headphones", "smartwatch", "camera", "tablet", "speaker", "monitor", "keyboard", "mouse"]
    products = []
    
    while len(products) < num_products:
        keyword = random.choice(keywords)
        if source == 'Amazon':
            result = scrape_amazon(keyword)
            products.extend(result['Amazon'])
        elif source == 'Flipkart':
            result = scrape_multiple_flipkart_products(keyword, num_products=3)
            products.extend(result)
        elif source == 'GeM':
            result = scrape_gem_products(keyword, num_results=3)
            products.extend(result)
        
        products = list({p['name']: p for p in products}.values())  # Remove duplicates
    
    return products[:num_products]

def main():
    trending_products = {
        'Amazon': get_random_products('Amazon'),
        'Flipkart': get_random_products('Flipkart'),
        'GeM': get_random_products('GeM')
    }
    
    with open('trending_products.json', 'w') as f:
        json.dump(trending_products, f, indent=2)

if __name__ == "__main__":
    main()