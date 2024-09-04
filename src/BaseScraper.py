import requests
from bs4 import BeautifulSoup
import re 



locations = ["vlorë", "sarandë"]
min_price = 40000
max_price = 120000
websites = ["Remax Albania"]

filters_applied = {
    "locations": locations,
    "min_price": min_price,
    "max_price": max_price,
    "websites": ["ReMax Albania", "Century21 Alb", "HomeZone"]
}

url_remax = "https://www.remax-albania.com/prona-me-qera-ne-{city}"

url_century = "https://www.century21albania.com/properties?display=grid&business_type=sale&city={city}&page="
url_homezone = "https://homezone.al/properties/sale/{city}?page="

# I have created this BaseScraper and we will use it to other Classes using Class Inheritance since this part of code we will use it to get the soup (template) of all wesbites

class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    import re

    def parse_price(self, price_string):
        try:
            # Use a regular expression to find numbers, including decimals
            parsed = re.findall(r'\d+\.?\d*', price_string)

            # Join the parts to form the full number as a string
            parsed_string = ''.join(parsed)

            # Convert to a float first
            parsed_value = float(parsed_string)

            # If the value is a whole number, convert it to an int
            if parsed_value.is_integer():
                return int(parsed_value)
            else:
                return parsed_value

        except ValueError as e:
        
            print(f"Parsing failed: {e}...{price_string}.")
            return None



    def fetch_and_parse(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        return BeautifulSoup(response.text, 'html.parser')


