import json

def get_products():
    try:
        with open('data/products.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_product(product):
    products = get_products()
    products.append(product)
    with open('data/products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
