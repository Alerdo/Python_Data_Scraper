# 🏡 Property Scraper Project

**Note**: Feel free to copy the logic and structure of this project. However, always make sure to check the terms and conditions of the websites before scraping, as many websites do not permit web scraping.

---

## 📖 Project Overview

I created the **Property_Data_Scraper Project** to automate the process of collecting real estate listings from multiple property websites. The project takes the scraped data, processes it, and sends daily email updates directly to my inbox. Leveraging Python’s powerful libraries, I built this solution to make tracking property listings easy, freeing me from the hassle of manual searching.

I loved working on this because it’s a perfect example of how a few scripts can automate mundane tasks and give you back your time. Plus, Python makes the whole process super easy with its powerful libraries.

---

## 💡 Key Features

- **Automated Web Scraping**: I scrape property listings from several websites, saving myself hours of searching manually.
- **Object-Oriented Practices**: I followed Object-Oriented Programming (OOP) principles to structure my code, using **class inheritance** to keep everything clean, organized, and reusable.
- **Data Cleansing and Processing**: Once the data is scraped, I clean and process it, applying filters based on price, location, and recency to get the most relevant listings.
- **Daily Email Notifications**: Every day, I get an email with neatly formatted property listings, keeping me up-to-date on the latest properties.
- **Scheduled Execution**: I scheduled the script to run automatically every day using PythonAnywhere, so it’s always working in the background.

---

## ⚙️ How It Works

Here’s a breakdown of how I built this project:

1. **Base Scraper Class**: I created a `BaseScraper` class to handle common functionality, like fetching HTML content and parsing prices. Each specific scraper inherits from this base class, making it easier to manage and reuse code.
   
2. **Individual Scraper Classes**:
   - `RemaxScraper`
   - `CenturyScraper`
   - `HomezoneScraper`

3. **Data Processing**: I wrote a `processor.py` script to clean the data. It cleans, formats the data, and standardizes the dates.

4. **Email Automation**: The `emailer.py` script I wrote sends out the property listings via email using a nice HTML template. I used Python's **smtplib** module for this, and I store all email configurations securely in an `.env` file.

5. **Scheduled Execution**: I’ve set the project to run every day using PythonAnywhere, but you can use any other scheduling systems.

---

## 🛠️ Technologies Used

Here are the tools and libraries I used for this project:

- **Python Libraries**:  `datetime`, `requests`, `os`, `BeautifulSoup`, `re`, `smtplib`, `dotenv` ect.
- **Object-Oriented Design**: I followed OOP principles to make the project scalable and easy to maintain.
- **Data Cleansing**: The scraped data is processed and cleaned before being sent, ensuring the emails only contain relevant and accurate listings.

---

## 🚀 Follow the instructions below to get started on a similar project

### 1. **Clone the repository**:
   First, clone the repository using the command below:

       git clone https://github.com/Alerdo/Python_Data_Scraper

### 2. **Set up a virtual environment**:
   To manage dependencies separately from the system environment, I recommend setting up a virtual environment:

       python -m venv venv  
       source venv/bin/activate  

### 3. **Install dependencies**:
   After activating the virtual environment, install the required libraries with:

       pip install -r 

### 4. **Configure your environment**:
   I use an `.env` file to store my email configurations securely. Your `.env` file should look something like this:

       SENDER_EMAIL=your-email@gmail.com  
       SENDER_AUTHENTICATOR=your-email-password  
       RECEIVERS=receiver1@gmail.com,receiver2@gmail.com

### 5. **Run the project**:
   To scrape the listings and send the email, run the main script:

       python main.py

### 6. **Schedule the task**:
   If you want to automate this process (like I did), you can set up a task scheduler. I used PythonAnywhere, and it was very easy to navigate.

   - **PythonAnywhere**: I recommend it for ease of use and setup. You can schedule the script to run daily without any hassle.

---

And that's how I automated the process of keeping track of property listings!

---

I'm always available to discuss, collaborate, and connect. Feel free to reach out through my Portfolio or LinkedIn.

<p align="center">
    <a href="https://alerdo-ballabani.co.uk/" target="_blank">
        <img src="https://img.shields.io/badge/Portfolio-Visit_My_Website-blue?style=for-the-badge" alt="Portfolio">
    </a>
    <a href="https://www.linkedin.com/in/alerdo-ballabani-450a85283/" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-Connect_With_Me-blue?style=for-the-badge" alt="LinkedIn">
    </a>
</p>

---

Feel free to connect!


