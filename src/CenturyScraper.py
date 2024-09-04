from BaseScraper import BaseScraper, min_price, max_price
class CenturyScraper(BaseScraper):

    def extract_listing(self, soup):
        listing = []

        # Loop through each property in the soup
        for prop in soup.find_all("div", class_="property"):
            # Find and extract the relevant elements
            price_tag = prop.find("h2", class_="text-primary mb-2")
            title_tag = prop.find("h5", class_="card-title")
            location_tag = prop.find("h6", class_="card-subtitle mt-1 mb-0 text-muted")
            area_tag = prop.find("div", class_="FutureInfo col-3")
            rooms_tag = prop.find("div", class_="FutureInfo col-3")
            photo_tag = prop.find("div", class_="card-img").find("img", class_="card-img-top")
            url_tag = prop.find("div", class_="card-list").find_all("a")[1]


            # Extract text or attributes
            price = self.parse_price(price_tag.get_text(strip=True))  if price_tag else "No price"
            title = title_tag.get_text(strip=True) if title_tag else "No title"
            location = location_tag.get_text(strip=True) if location_tag else "No location"
            area = area_tag.get_text(strip=True).replace("m²", "").strip() if area_tag else "No area"
            rooms = rooms_tag.get_text(strip=True) if rooms_tag else "No rooms"

            photo = photo_tag["data-src"] if photo_tag and "data-src" in photo_tag.attrs else "No photo"
            url = url_tag["href"] if url_tag else "No URL"

            # Append the data to the listing list
            if price is not None and min_price <= price <= max_price:
                listing.append({
                    "website": "Century",
                    "price": price,
                    "title": title,
                    "location": location,
                    "area": area,
                    "rooms": rooms,
            
                    "photo": photo,
                    "url": url
                })

        return listing

    # Main function to fetch results across multiple pages
    def fetch_all_pages(self, base_url):
        page_nr = 1
        all_listings = []

        while True:
            url = f"{base_url}{page_nr}"
            soup = self.fetch_and_parse(url) # from the BaseScrapper
 

            if soup is None:
                break
         

            # Extract info from the current page
            listings = self.extract_listing(soup)
          
            if not listings:
                break

            # Extend the list of all listings
            all_listings.extend(listings)
            

            # Check if there are other pages to scrape data
            pagination = soup.find("ul", class_="pagination")
            
            # Checking if there are any pages
            # if not pagination or "active" not in [li["class"][1] for li in pagination.find_all("li") if "class" in li.attrs and len(li["class"]) > 1]:

            #     break
            
            if page_nr == 5:
                break
            page_nr += 1

        return all_listings




# base_url  = "https://www.century21albania.com/properties?display=grid&business_type=sale&city=Vlor%C3%AB&page="
# century_scraper_vlore = CenturyScraper(base_url)

# century_data = century_scraper_vlore.fetch_all_pages(base_url)

# url_century = "https://www.century21albania.com/properties?display=grid&business_type=sale&city=sarande&page="

# sarande_scraper = CenturyScraper(url_century)
# sarande_data = sarande_scraper.fetch_all_pages(url_century)

# century_data.extend(sarande_data)

# print(len(century_data))
# for prop in century_data:
#     print(prop)

