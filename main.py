from flask import Flask, render_template, request
from amazon_price_scraper import get_item_name, get_item_price, add_item, update_prices, export_item_list, get_tracked_items

app = Flask(__name__)

@app.route('/')
def home():
    items = get_tracked_items()
    return render_template('listItems.html', items=items)

@app.route('/add')
def add_item_get():
    return render_template('addItem.html')

@app.route('/add', methods=['POST'])
def add_item_post():
    item_link = request.form['link']
    add_item(item_link)
    try:
        item_name = get_item_name(item_link)
        return f"Item {item_name} has been added!"
    except:
        return "An error occurred!"

@app.route('/item_price')
def item_price_get():
    return render_template('itemPrice.html')

@app.route('/item_price', methods=['POST'])
def item_price_post():
    item_link = request.form['link']
    try:
        item_price = get_item_price(item_link)
        return f"The item is priced at {item_price}"
    except:
        return "An error occurred!"
    
@app.route('/update_prices')
def update_prices_get():
    update_prices()
    return "Prices have been updated!"

@app.route('/export')
def export_get():
    export_item_list()
    return "Items have been exported!"



if __name__ == '__main__':
    app.run(debug=True)