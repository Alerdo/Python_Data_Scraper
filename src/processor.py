from Remax_Sraper import RemaxScraper
from CenturyScraper import CenturyScraper
from HomezoneScraper import HomezoneScraper
from datetime import datetime

# Process data - it will clean the data, e.g., form the full URL of each property
def clean_data(listings):
    processed_listings = []
    sorted_listing = sorted(listings, key=lambda x: x["price"])
    for listing in sorted_listing:

        listing["price"] = f"€{int(listing['price']):,}"
        listing['processed'] = True  # Mark the record as processed
        
        processed_listings.append(listing)
        if "date" in listing:
             if isinstance(listing["date"], datetime):
                 listing["date"] = listing["date"].strftime("%d/%m/%Y")
    
    
    return processed_listings





def get_clean_data(url_remax, url_century, url_homezone):
    ## Creating the class instances for each object
    remax_scraper = RemaxScraper(url_remax)
    century_scraper  = CenturyScraper(url_century)
    homezone_scraper = HomezoneScraper(url_homezone)

    ## Fetch all data
    remax_data = remax_scraper.fetch_all_pages(url_remax)
    century_data = century_scraper.fetch_all_pages(url_century)
    homezone_data = homezone_scraper.fetch_all_pages(url_homezone)
    


    all_listings = []
    all_listings.extend(remax_data)
    all_listings.extend(century_data)
    all_listings.extend(homezone_data)
    if all_listings:
        processed_listings = clean_data(all_listings) 
        for listing in processed_listings:
            print(listing)
    else:
        print("No data to process")

    return all_listings



# This function it will call the get_data, however it will call it with diffrent cities, hence the for loop
def fetch_all_cities(cities_list, url1, url2, url3):
        final_result = []
        for city in cities_list:
            if city == "vlorë":
                 url1_formated = url1.format(city="vlore")
            elif city == "sarandë":
                 url1_formated = url1.format(city="sarande")
            
            url2_formated = url2.format(city=city)
            url13_formated = url3.format(city=city)
           

            all_cities_data = get_clean_data(url1_formated, url2_formated, url13_formated)
            final_result.extend(all_cities_data)
        return final_result



