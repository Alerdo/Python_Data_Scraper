
from emailer import send_email
from BaseScraper import locations, url_remax, url_century, url_homezone
from processor import fetch_all_cities
import re

def extract_price(price_str):
    cleaned_price = re.sub(r"[^\d.]", "", price_str)
    return float(cleaned_price)



def  main(locations, url_remax, url_century, url_homezone):
    # Fetch and process data
    
    all_listings = fetch_all_cities(locations, url_remax, url_century, url_homezone)
    sorted_listings = sorted(all_listings, key=lambda x: extract_price(x["price"])) # I am using this to extract the price and sort by that price whithout altering "price" key
    # Send processed data via email
    if all_listings:
        send_email(sorted_listings)
        return {
            'statusCode': 200,
            'body': 'Email sent successfully with listings.'
        }
    else:
        return {
            'statusCode': 200,
            'body': 'No listings to email today.'
        }


if __name__ == "__main__":
     main(locations, url_remax, url_century, url_homezone)