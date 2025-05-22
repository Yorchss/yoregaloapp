from packaging.version import Version
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

url=""
def scrape_products(url):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1920,1080")

    driver = uc.Chrome(options=options)
    driver.get(url)

    # Wait for JS to load
    time.sleep(5)

    product_elements = driver.find_elements(By.CLASS_NAME, "product")
    print(f"Found {len(product_elements)} product elements")

    products = []

    for product in product_elements:
        try:
            image_tag = product.find_element(By.TAG_NAME, "img")
            image_url = image_tag.get_attribute("data-src")
            if not image_url or not image_url.endswith(".jpg"):
                image_url = "No image found"
        except:
            image_url = "No image found"

        try:
            price = product.get_attribute("data-price")
            if not price:
                price = "No price found"
        except:
            price = "No price found"

        products.append({"image": image_url, "price": price})

    driver.quit()
    return products
