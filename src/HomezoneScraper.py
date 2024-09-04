import sys
import io
from datetime import datetime, timedelta    
from BaseScraper import BaseScraper
import re

# Set the default encoding to UTF-8 to handle special characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class HomezoneScraper(BaseScraper):

    def extract_listing(self, soup):
        listing = []

        for prop in soup.find_all("article", class_="property-body"):

            # Find each tag within the property listing
            price_tag = prop.find("div", class_="header-primary center-flex").find('span')
            title_tag = prop.find("h2", class_="header-small-2")
            link_tag = prop.find("a", class_="link-title")
            location_tag = prop.find("p", class_="property-address")
            photo_tag = prop.find("div", class_="property-main-image").find('img')
            rooms_list = prop.find_all("div", class_="property-rooms-info")
            date_tag = prop.find("strong")

            # Extracting information with checks
            price = price_tag.get_text(strip=True) if price_tag else "No price"
            price =  self.parse_price(price)  if price != "No Price" else "No Price"
            title = title_tag.get_text(strip=True) if title_tag else "No title"
            link = link_tag['href'] if link_tag else "No URL"
            # print(link)
            link =  "https://homezone.al" + link     if link != "No URL" else "No URL"
            # print (f"this is formated   {link}")
            location = location_tag.get_text(strip=True) if location_tag else "No location"
            photo = photo_tag['src'] if photo_tag else "No photo"
            date = date_tag.get_text(strip=True) if date_tag else "No date" 
            date = datetime.strptime(date, "%d/%m/%Y")
            # Assuming there is a specific order: rooms first, then bathrooms, and then surface area.
            rooms = rooms_list[0].get_text(strip=True) if len(rooms_list) > 0 else "No rooms info"
            bathrooms = rooms_list[1].get_text(strip=True) if len(rooms_list) > 1 else "No bathrooms info"
            surface = rooms_list[2].get_text(strip=True) if len(rooms_list) > 2 else "No surface info"

            six_months_ago = datetime.now() - timedelta(days=30*4)


            if (price is not None and 120000 >= price >= 40000) and (date =="No date" or  date >= six_months_ago ):
                # Append to the listing if necessary conditions are met
                listing.append({
                    "website": "Homezone",
                    "title": title,
                    "price": price,
                    "location": location,
                    "rooms": rooms,
                    "bathrooms": bathrooms,
                    "surface": surface,
                    "photo": photo,
                    "url": link,
                    "date": date
                })

        return listing

    def fetch_all_pages(self, base_url):
        page_nr = 1 
        all_listing = []
        
        while True:
            
            url = f"{base_url}{page_nr}"
            soup = self.fetch_and_parse(url)

            listing = self.extract_listing(soup)

            
            # limit_date = datetime.strptime("01-01-2023", "%d-%m-%Y")

            # for prop in listing:
            #     prop_date = datetime.strptime(prop["date"], "%d/%m/%Y")
            #     prop["date"] = prop_date.strftime("%d/%m/%y")
                
            #     if prop_date < limit_date:
            #         break

            if not listing:
                break

            # print(f"Page: {page_nr}, Listings Found: {len(listing)}")

            if listing:
                all_listing.extend(listing)

            pagination = soup.find("ul", class_="pagination")

            
            if not pagination or page_nr == 15:
                break
            
            page_nr += 1

        return all_listing

# url_homezone = "https://homezone.al/properties/sale/vlore?page="

# homezone_scraper = HomezoneScraper(url_homezone)
# data = homezone_scraper.fetch_all_pages(url_homezone)

# print(len(data))
# for prop in data:
#     print(prop)