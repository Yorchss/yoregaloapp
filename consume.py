from flask import Flask, request, jsonify, render_template
from app import scrape_products

app = Flask(__name__)

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    try:    
        #if request.method == 'GET':
            #return jsonify({'error': 'This endpoint only accepts POST requests'}), 405
        data = request.get_json()
        url = data.get('url')
        products = scrape_products(url)
        return jsonify(products)
    except Exception as e:
        import traceback
        print("❌ Error during scraping:", e)
        traceback.print_exc()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
