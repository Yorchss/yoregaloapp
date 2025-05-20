from flask import Flask, jsonify, render_template

import requests
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder="static")

def scrape_product(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch the page"}
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract only JPG images
    jpg_images = [img.get("src") for img in soup.find_all("img") if img.get("src", "").endswith(".jpg")]
    jpg_image = jpg_images[0] if jpg_images else "No JPG image found"

     # Extract price (modify selector based on site structure)
    price_tag = soup.find(class_="product_price")  # Replace with actual class name
    price = price_tag.text.strip() if price_tag else "No price found"
    price = soup.find("input", {"name": "product_price"})["value"]

    return {"image": jpg_image, "price": price}
    

@app.route('/product')
def product_api():
    url = "https://www.enviaflores.com/florerias-nuevo-leon/monterrey/2386"  # Replace with actual product URL
    product_data = scrape_product(url)
    return jsonify(product_data)

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)