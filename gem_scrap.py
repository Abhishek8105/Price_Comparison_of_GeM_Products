import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import re
def search_products(keyword, num_results=20):
    search_query = f"{keyword} site:https://mkp.gem.gov.in"
    google_url = f"https://www.google.com/search?q={search_query}&num={num_results}"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    response = requests.get(google_url, headers={'User-Agent': user_agent})
    soup = BeautifulSoup(response.text, 'lxml')   
    search_results = []
    for result in soup.find_all('div', class_='yuRUbf'):
        link = result.find('a', href=True)
        if link and 'mkp.gem.gov.in' in link['href']:
            search_results.append(link['href'])
    return search_results[:num_results]
def get_product_details(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    response = requests.get(url, headers={'User-Agent': user_agent})
    soup = BeautifulSoup(response.text, 'lxml')

    # Extract product name
    title_div = soup.find('div', {'id': 'title'})
    product_name = title_div.find('h1', {'itemprop': 'name'}).text.strip() if title_div else None

    # Extract image URL
    image_span = soup.find('span', attrs={'data-src': True})
    image_url = image_span['data-src'] if image_span else None

    # Get the lowest price
    lowest_price = get_lowest_price(url)

    if product_name and image_url and lowest_price != "N/A":
        return {
            'name': product_name,
            'image_url': image_url,
            'price': lowest_price,
            'product_url': url,
        }
    return None

def get_lowest_price(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    response = requests.get(url, headers={'User-Agent': user_agent})
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Try to find the "All Sellers" link
    all_sellers_link = soup.find('a', class_='sellers_summary')
    if all_sellers_link:
        all_sellers_url = urljoin(url, all_sellers_link['href'])
        response = requests.get(all_sellers_url, headers={'User-Agent': user_agent})
        soup = BeautifulSoup(response.text, 'lxml')

    rows = soup.find_all('tr')
    lowest_price = float('inf')

    for row in rows:
        offer_price_td = row.find('td', class_='offer-price')
        if offer_price_td:
            price_text = offer_price_td.get_text(strip=True)
            price = float(re.sub(r'[^\d.]', '', price_text))
            if price < lowest_price:
                lowest_price = price

    return "{:.2f}".format(lowest_price) if lowest_price != float('inf') else "N/A"

def scrape_gem_products(keyword, min_results=15):
    products = []
    num_results = min_results
    
    while len(products) < min_results:
        product_urls = search_products(keyword, num_results)
        
        for url in product_urls:
            product_info = get_product_details(url)
            if product_info:
                products.append(product_info)
                if len(products) >= min_results:
                    break
        
        num_results += 5  # Increase the number of results to search if we don't have enough products
    
    return products

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    categories = ["Electronics", "Clothing", "Furniture", "Books"]
    all_products = {}

    for category in categories:
        print(f"Searching for '{category}' on GeM...")
        products = scrape_gem_products(category, 15)
        all_products[category] = products
        print(f"Found {len(products)} products for {category}")

    save_to_json(all_products, 'gem_products.json')
    print("Products saved to gem_products.json")