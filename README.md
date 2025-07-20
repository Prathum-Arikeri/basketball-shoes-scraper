# Basketball Shoes Scraper

A Python project that uses Selenium and BeautifulSoup to scrape **men's basketball shoes** and their prices from the official 
Nike, Under Armour, Puma, and Way of Wade websites.

## Project Description
This script automates Chrome to:
- Load the full pages (including dynamically loaded products)
- Scroll to trigger loading all products
- Parse each product's name, price, and URL
- Save the scraped data to a CSV file (`data/shoes.csv`)

This project is part of my effort to build real-world Python skills in web scraping, automation, and data collection.

---

## How to run

**Clone this repository**
```bash
git clone https://github.com/Prathum-Arikeri/basketball-shoes-scraper.git
cd basketball-shoes-scraper
```

**Create & activate virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
```

**Install required packages**
```bash
pip install -r requirements.txt
```

**Run the scraper**
```bash
python scraper.py
```
## Output
```bash
The scraper prints product names and prices in the terminal 
and saves them to `data/shoes.csv`.
```