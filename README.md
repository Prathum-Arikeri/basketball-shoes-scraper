# Basketball Shoes Scraper

A Python project that uses Selenium and BeautifulSoup to scrape **Nike men's basketball shoes** and their prices from the official Nike website.

## Project Description
This script automates Chrome to:
- Load the full page (including dynamically loaded products)
- Scroll to trigger loading all 47 products
- Parse each product's name and price
- Print them in the terminal

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
