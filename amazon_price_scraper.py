from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json

tracked_items = []

def get_tracked_items():
    return tracked_items

def get_item_name(url):
    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.content, 'html.parser')
    item_name = soup.find('span', id='productTitle').text
    return item_name

def get_item_price(url):
    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.content, 'html.parser')
    whole = soup.find_all('span', class_='a-price-whole')
    fraction = soup.find_all('span', class_='a-price-fraction')
    return whole[0].text + fraction[0].text

def add_item(url):
    name = get_item_name(url)
    price = get_item_price(url)
    # Check if the item is already being tracked
    for item in tracked_items:
        if item['url'] == url:
            return "Item is already being tracked!"
    else:
        # If the item is not being tracked, add it with the initial price history
        current_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        tracked_items.append({'url': url, 'name': name, 'price_history': {current_date: price}})
    return f"Item {get_item_name(url)} has been added!"

def update_prices():
    for item in tracked_items:
        price = get_item_price(item['url'])
        current_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        item['price_history'][current_date] = price

def export_item_list():
    with open('tracked_items.json', 'w') as file:
        json.dump(tracked_items, file, indent=4)

def load_item_list():
    global tracked_items
    try:
        with open('tracked_items.json', 'r') as file:
            tracked_items = json.load(file)
            print("Loading item list from file...")
    except FileNotFoundError:
        tracked_items = []
        print("No item list found, starting with empty list...")

load_item_list()
