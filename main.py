from flask import Flask, jsonify
import requests
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to scrape gas prices from a website (GasBuddy)
def get_santa_barbara_gas_prices():
    # Send a GET request to GasBuddy (or any other website with gas prices)
    url = 'https://www.gasbuddy.com/gasprices/california/santa-barbara'
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Unable to fetch data from GasBuddy"}

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the gas stations and their prices
    gas_stations = soup.find_all('div', class_='styles__station___2zIUl')

    if not gas_stations:
        return {"error": "No gas stations found"}

    prices = []
    for station in gas_stations:
        # Extract station name
        station_name = station.find('span', class_='styles__name___3LIl7')
        if station_name:
            station_name = station_name.get_text(strip=True)
        else:
            station_name = "Unknown"

        # Extract price
        price = station.find('span', class_='styles__price___16z44')
        if price:
            price = price.get_text(strip=True)
        else:
            price = "N/A"

        # Append to list
        prices.append({
            'station_name': station_name,
            'price': price
        })

    return prices

@app.route('/')
def index():
    return "Welcome to the Gas Price API!"

@app.route('/gasprices/santa-barbara', methods=['GET'])
def get_santa_barbara_gas_prices_route():
    # Get the gas prices
    gas_prices = get_santa_barbara_gas_prices()

    if "error" in gas_prices:
        return jsonify(gas_prices), 500
    else:
        return jsonify(gas_prices)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))  # Changed to port 3000 for Replit