import requests
from bs4 import BeautifulSoup

# url = "https://www.remax-albania.com/prona-me-qera-ne-vlore/"
# url2 = "url1website"
# url3 = "url1website"
# url4 = "url1website"
# url5 = "url1website"

locations = ["vlore", "sarande"]
min_price = 40000
max_price = 120000
websites = ["Remax Albania"]

filters_applied = {
    "locations": locations,
    "min_price": min_price,
    "max_price": max_price,
    "websites": websites
}


## Inital function to return the soup object 
def fetch_and_parse(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Successfully fetched content from {url}")


        # Parsing the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    

def parse_price(price_string):
    try:
        # Remove commas and currency symbols, then strip whitespace
        parsed = price_string.replace(",", "").replace("€", "").strip()

        # Check if the parsed string is numeric
        if parsed.isdigit():
            return int(parsed)
        else:
            print(f"Skipping non-numeric price: {price_string}")
            return None
    except ValueError as e:
        print(f"Parsing failed: {e}")
        return None


def extract_listing(soup):
    listing = []

    for prop in soup.find_all("div", "gallery-item-container"):

        ##First for each prop using the loop we will find the first instance of each tagg using find()

        title_tag = prop.find("div", class_="gallery-title")
        price_tag = prop.find('a', class_='proplist_price')
        location_tag = prop.find("a", title=True)
        type_tag = prop.find("div", class_="gallery-transtype")
        photo_tag = prop.find("div", class_="gallery-photo").find('img')
        agent_tag = prop.find("img", class_="agent-face")
        url_tag = prop.find("div", class_="gallery-photo").find('a')
        no_rooms_list = prop.find("div", class_="gallery-icons").find_all("span", class_="gallery-attr-item-value")

        #Below we check if each tagg returns something and we extract the information 
        title = title_tag.get_text(strip=True)   if title_tag else "No title"
        price = parse_price(price_tag.get_text(strip=True)) if price_tag else "No price"
        location = location_tag.get_text(strip=True) if location_tag else "No location"
        type_prop = type_tag.get_text(strip=True) if type_tag else "No property type"
        photo = photo_tag['data-src'] if photo_tag and 'data-src' in photo_tag.attrs else "No photo"
        agent_name = agent_tag["alt"] if agent_tag else "No agent name shown"
        property_url = url_tag['href'] if url_tag else "No URL"
        no_rooms_list = prop.find("div", class_="gallery-icons").find_all("span", class_="gallery-attr-item-value")
        if len(no_rooms_list) > 1:
            no_rooms_tag = no_rooms_list[1]
            no_rooms = no_rooms_tag.get_text(strip=True) if no_rooms_tag else "Number of rooms not given"
        else:
            no_rooms = "Number of rooms not given"


        if price is not None and min_price <= price <= max_price:
            listing.append({
                "title": title, 
                "price": price, 
                "location": location,
                "type": type_prop,
                "rooms": no_rooms,
                "photo": photo,
                "agent": agent_name,
                "url": property_url
            }) 

    return listing

# The below we have the MAIN function whos purpose is to search results in a few pages not just the given url (if there is any)
# This function is the one who calles the intial function fetch_and_parse(url) to get the soup, 
# it than calls extract listings 
# it will extract listings as long as the loop doesnt break, the loop can break if no other page is not found 
# it returns the list with all properties which is coming from extract_listing(soup)
def fetch_all_pages(base_url):

    page_nr = 1
    all_listings = []

    while True:
        url = f"{base_url}?CurrentPage={page_nr}"
        soup = fetch_and_parse(url)

        if soup is None:
            break

        ##Extract info from the current page
        listings = extract_listing(soup)

        if not listings:
            break

        ##Exteds used for lists
        all_listings.extend(listings)

        #Check if there are other pages to scrap data

        pagination = soup.find("ul", class_="pagination")
        
        # Checking if there are any pages, using if statment, to check if there is an ajax-page-link on the list return from list comprehension
        if not pagination or "ajax-page-link" not in [li["class"][0] for li in pagination.find_all("li") if "class" in li.attrs]:
            break

        page_nr += 1

    return all_listings


