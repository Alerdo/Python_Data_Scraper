from BaseScraper import BaseScraper, min_price, max_price


class RemaxScraper(BaseScraper):    



    def extract_listing(self, soup):
        listing = []

        for prop in soup.find_all("div", "gallery-item-container"):

            # First for each prop using the loop we will find the first instance of each tag using find()

            title_tag = prop.find("div", class_="gallery-title")
            price_tag = prop.find('a', class_='proplist_price')
            location_tag = prop.find("a", title=True)
            type_tag = prop.find("div", class_="gallery-transtype")
            photo_tag = prop.find("div", class_="gallery-photo").find('img')
            agent_tag = prop.find("img", class_="agent-face")
            url_tag = prop.find("div", class_="gallery-photo").find('a')
            no_rooms_list = prop.find("div", class_="gallery-icons").find_all("span", class_="gallery-attr-item-value")

            # Below we check if each tag returns something and we extract the information 
            title = title_tag.get_text(strip=True) if title_tag else "No title"
            price = self.parse_price(price_tag.get_text(strip=True)) if price_tag else "No price"
            location = location_tag.get_text(strip=True) if location_tag else "No location"
            type_prop = type_tag.get_text(strip=True) if type_tag else "No property type"
            photo = photo_tag['data-src'] if photo_tag and 'data-src' in photo_tag.attrs else "No photo"
            agent_name = agent_tag["alt"] if agent_tag else "No agent name shown"
            property_url = url_tag['href'] if url_tag else "No URL"
            property_url = f"https://www.remax-albania.com{property_url}" if property_url != "No URL" else "No Url"
            
            if len(no_rooms_list) > 1:
                no_rooms_tag = no_rooms_list[1]
                no_rooms = no_rooms_tag.get_text(strip=True) if no_rooms_tag else "Number of rooms not given"
            else:
                no_rooms = "Number of rooms not given"

            if price is not None and min_price <= price <= max_price:
                listing.append({
                    "website": "Remax",
                    "title": title, 
                    "price": price, 
                    "location": location,
                    # "type": type_prop,
                    "rooms": no_rooms,
                    "photo": photo,
                    "agent": agent_name,
                    "url": property_url
                }) 

        return listing

    # Main function to fetch results across multiple pages
    def fetch_all_pages(self, base_url):
        page_nr = 1
        all_listings = []
        
        while True:
            url = f"{base_url}?CurrentPage={page_nr}"

            soup = self.fetch_and_parse(url) # here is the soup . we can use self to acces it

            if soup is None:
                break

            # Extract info from the current page
            listings = self.extract_listing(soup)

            # Extend the list of all listings
            all_listings.extend(listings)

            # Check if there are other pages to scrape data
            pagination = soup.find("ul", class_="pagination")
            
            #Checking if there are any pages
            if not pagination or "ajax-page-link" not in [li["class"][0] for li in pagination.find_all("li") if "class" in li.attrs]:
                break
           
            page_nr += 1

        return all_listings


