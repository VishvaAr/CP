import requests

# Your API Key
API_KEY = "olNnH6iSyPabk6zGefAKF6J3B5VW30dCmCMSr1Wh"
BASE_URL = "https://api.eia.gov/v2/petroleum/pri/spt/data/"

# Query parameters for California (Los Angeles) gas prices
params = {
    "api_key": API_KEY,
    "frequency": "annual",
    "data[0]": "value",
    "facets[duoarea][0]": "Y05LA",  # Los Angeles Duoarea code (for California gas prices)
    "facets[product][0]": "EPMRR",    # Regular Gasoline Price
    "start": "2010",
    "end": "2024",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc"
}

def fetch_california_gas_prices():
    try:
        # Perform the API request
        response = requests.get(BASE_URL, params=params)
        print("Request URL:", response.url)  # Debugging: print full request URL
        
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            print("Full API Response:", data)  # Debugging: print the entire response
            return data.get("response", {}).get("data", [])
        else:
            # Print error details
            print(f"Error: {response.status_code}")
            print("Response Text:", response.text)
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def print_california_gas_prices(prices):
    if not prices:
        print("No gas prices to display.")
        return
    
    print("California Annual Gas Prices (Los Angeles):")
    for record in prices:
        year = record.get("period", "N/A")
        value = record.get("value", "N/A")
        value = float(value)
        local_tax = value * 0.0225;
        adjusted_price = value + 0.85 + 0.10 + 0.30 + local_tax
        print(f"Year: {year}, Price: {adjusted_price:.3f}")

if __name__ == "__main__":
    # Fetch and print gas prices for California (Los Angeles)
    gas_prices = fetch_california_gas_prices()
    
    # Print gas prices
    if gas_prices:
        print_california_gas_prices(gas_prices)
    else:
        print("No data fetched from the API.")