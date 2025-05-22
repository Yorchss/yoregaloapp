from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__, static_folder="static")

# Target URL
URL = "https://www.enviaflores.com/florerias-nuevo-leon/monterrey?cs=todas-las-flores"

# Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/"
}

print(URL)  # Removed incorrect indentation

def scrape_products(URL):
    print(URL)
    response = requests.get(URL, headers=HEADERS)
    print(response.text[:500])
    
    if response.status_code != 200:
        print("Error fetching the page")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    print(f"Status code: {response.status_code}")
    print(f"Response length: {len(response.text)}")

    products = []

    # Modify these selectors based on actual HTML structure
    product_containers = soup.find_all(class_="product-container")  # Update class name accordingly
    product_containers = soup.find_all("div", class_="product")

    print(f"Found {len(product_containers)} product containers")

    for product in product_containers:
        image_tag = product.find("img")
        image_url = image_tag["data-src"] if image_tag and image_tag.get("data-src", "").endswith(".jpg") else "No image found"
        price = product.get("data-price", "No price found")
    
        products.append({"image": image_url, "price": price})

    return products

@app.route('/product')
def product_api():
    product_data = scrape_products(URL)
    return jsonify(product_data)

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)