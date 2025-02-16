import json

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Load the original JSON file
    products = load_json('gem_products.json')
    
    # Create a new dictionary for frontend use
    frontend_products = {}
    
    # Process each category
    for category, category_products in products.items():
        # Include all products (minimum 15) with complete details
        frontend_products[category] = [
            {
                'name': product['name'],
                'image_url': product['image_url'],
                'price': product['price'],
                'product_url': product['product_url']
            }
            for product in category_products
        ]
    
    # Save the processed data to a new JSON file for frontend use
    save_json(frontend_products, 'gem_products_frontend.json')
    print("Frontend product data has been saved to gem_products_frontend.json")