from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__, static_folder="static")

# Target URL
URL = "https://www.enviaflores.com/florerias-nuevo-leon/monterrey?cs=todas-las-flores"

# Headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_products(url):
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print("Error fetching the page")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    # Modify these selectors based on actual HTML structure
    product_containers = soup.find_all(class_="product-container")  # Update class name accordingly
    product_containers = soup.find_all("div", class_="product")
    
    for product in product_containers:
        image_tag = product.find("img")
        #price_tag = product.find(class_="data-price")  # Update class based on site
        
        image_url = image_tag["data-src"] if image_tag and image_tag.get("data-src", "").endswith(".jpg") else "No image found"
        #price = price_tag["data-price"].text.strip() if price_tag else "No price found"
        price = product.get("data-price", "No price found")
        
       
        products.append({"image": image_url, "price": price})

    return products

@app.route('/product')
def product_api():
    product_data = scrape_products(URL)
    #print(json.dumps(product_data, indent=4))
    return jsonify(product_data)

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)