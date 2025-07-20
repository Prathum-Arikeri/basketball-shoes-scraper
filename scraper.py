from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import random
import json
import sqlite3
import pandas as pd
import re

def human_like_scroll(driver, pause_time=1.5, scroll_increment=300):
    """Scroll down the page slowly in increments with random pauses."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_pos = 0

    while current_pos < last_height:
        current_pos += scroll_increment
        driver.execute_script(f"window.scrollTo(0, {current_pos});")
        time.sleep(pause_time + random.uniform(0.5, 1.5))
        last_height = driver.execute_script("return document.body.scrollHeight")

# Not needed for now because I initially will only tackle sites without strict CAPTCHA
def wait_manual_bypass(wait_time=30):
    '''
    print(f"Pausing for {wait_time} seconds for manual CAPTCHA bypass (or just a break)...")
    for remaining in range(wait_time, 0, -1):
        print(f"Continuing in {remaining} seconds...", end='\r')
        time.sleep(1)
    print("\nResuming scraping now.")
    '''
    pass

def scrape_nike():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    url = 'https://www.nike.com/w/mens-basketball-shoes-3glsmznik1zy7ok'

    driver.get(url)
    time.sleep(2)

    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    container = soup.find('div', id='skip-to-products')
    shoes = container.find_all('div', attrs={'data-product-position': True})
    products = []

    for shoe in shoes:
        name_tag = shoe.find('a', class_='product-card__link-overlay')
        price_tag = shoe.find('div', class_='product-price')
        image_tag = shoe.find('img', class_='product-card__img')

        if name_tag and price_tag:
            product_name = name_tag.text.strip()
            product_price = price_tag.text.strip()
            product_url = name_tag['href']
            product_image = image_tag['src'] if image_tag else None

            products.append({
                'name': product_name,
                'price': product_price,
                'url': product_url,
                'image': product_image
            })
            print(product_name, product_price, product_url, product_image)

    driver.quit()
    return products

# Experimental StockX scraper — may not work due to captcha/bot detection
def scrape_stockx():
    '''
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    SCROLL_PAUSE_TIME = 2
    products = []

    url = 'https://stockx.com/search?category=performance&gender=men&mens-shoe-size=US+M+10&s=mens+basketball+shoes'
    driver.get(url)
    time.sleep(2)  # let page start loading
    wait_manual_bypass(30)

    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    pagination = soup.find_all('li', class_='chakra-pagination__page')
    total_pages = 1
    if pagination:
        try:
            total_pages = int(pagination[-1].text.strip())
        except:
            pass

    print(f"Found {total_pages} pages to scrape.")

    for page in range(1, total_pages + 1):
        print(f"Scraping page {page}...")
        url = f'https://stockx.com/search?category=performance&gender=men&mens-shoe-size=US+M+10&s=mens+basketball+shoes&page={page}'
        driver.get(url)

        time.sleep(2)

        human_like_scroll(driver, pause_time=1.5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        shoes = soup.find_all('div', attrs={'data-testid': 'product-card'})

        for shoe in shoes:
            name_tag = shoe.find('p', attrs={'data-testid': 'product-tile-title'})
            price_tag = shoe.find('p', attrs={'data-testid': 'product-tile-lowest-ask-amount'})
            image_tag = shoe.find('img', class_='chakra-image')
            url_tag = shoe.find('a', href=True)

            if name_tag and price_tag:
                product_name = name_tag.text.strip()
                product_price = price_tag.text.strip()
                product_image = image_tag['src'] if image_tag else None
                product_url = 'https://stockx.com' + url_tag['href'] if url_tag else None

                products.append({
                    'name': product_name,
                    'price': product_price,
                    'url': product_url,
                    'image': product_image
                })

                print(product_name, product_price, product_url, product_image)

    driver.quit()
    print(f"\nScraped {len(products)} products from StockX across {total_pages} pages")
    return products
    '''
    pass

def scrape_goat():
    # TODO: implement GOAT scraper
    # Return list of dicts with keys: name, price, url, image
    return []

def scrape_ua():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    url = 'https://www.underarmour.com/en-us/c/shoes/basketball/mens+adult_unisex/'

    driver.get(url)
    time.sleep(3)

    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    name_tags = soup.find_all('a', class_='ProductTile_product-item-link__tSc19')
    products = []

    for name_tag in name_tags:
        parent = name_tag.parent

        sub_header = parent.find('span', class_='ProductTile_product-sub-header__WUmwg')
        if sub_header and 'Basketball Shoes' in sub_header.text:
            product_name = name_tag.text.strip()
            product_url = 'https://www.underarmour.com' + name_tag['href']

            price_tag = parent.find_next('div', class_='PriceDisplay_sr-price__NA35y')
            product_price = price_tag.text.strip() if price_tag else 'Price not found'

            image_tag = parent.find('img')
            product_image = image_tag['src'] if image_tag and image_tag.has_attr('src') else None

            products.append({
                'name': product_name,
                'price': product_price,
                'url': product_url,
                'image': product_image
            })

            print(product_name, product_price, product_url, product_image)

    driver.quit()
    print(f"\nFound {len(products)} basketball shoes on Under Armour")
    return products

def scrape_puma():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    url = 'https://us.puma.com/us/en/men/shoes/basketball?offset=0'
    driver.get(url)
    time.sleep(2)

    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    product_links = soup.find_all('a', attrs={'data-test-id': 'product-list-item-link'})

    products = []

    for link in product_links:
        name_tag = link.find('h3')
        product_name = name_tag.text.strip() if name_tag else 'Name not found'

        href = link.get('href')
        product_url = 'https://us.puma.com' + href if href else None

        image_tag = link.find('img')
        product_image = image_tag['src'] if image_tag and image_tag.has_attr('src') else None

        sale_price_tag = link.find('span', attrs={'data-test-id': 'sale-price'})
        regular_price_tag = link.find('span', attrs={'data-test-id': 'price'})

        if sale_price_tag:
            product_price = sale_price_tag.text.strip()
        elif regular_price_tag:
            product_price = regular_price_tag.text.strip()
        else:
            product_price = 'Price not found'

        products.append({
            'name': product_name,
            'price': product_price,
            'url': product_url,
            'image': product_image
        })

        print(product_name, product_price, product_url, product_image)

    driver.quit()
    print(f"\nFound {len(products)} basketball shoes on Puma")
    return products

def scrape_wayofwade():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    url = 'https://wayofwade.com/collections/basketball-shoes'
    driver.get(url)
    time.sleep(2)

    SCROLL_PAUSE_TIME = 2
    max_attempts_without_new = 5
    attempts = 0

    last_height = driver.execute_script("return document.body.scrollHeight")

    while attempts < max_attempts_without_new:
        driver.execute_script("""
            window.scrollTo(0, document.body.scrollHeight * 0.9);
        """)
        time.sleep(SCROLL_PAUSE_TIME)

        driver.execute_script("""
            window.scrollTo(0, document.body.scrollHeight);
        """)
        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            attempts += 1
        else:
            attempts = 0
        last_height = new_height

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    products = []

    product_divs = soup.find_all('div', class_='t4s-product')

    for product in product_divs:
        name_tag = product.find('h3', class_='t4s-product-title')
        url_tag = name_tag.find('a') if name_tag else None

        product_name = name_tag.text.strip() if name_tag else 'Name not found'

        if 'slide' in product_name.lower():
            continue

        product_url = url_tag['href'] if url_tag and url_tag.has_attr('href') else None
        if product_url and product_url.startswith('/'):
            product_url = 'https://wayofwade.com' + product_url

        price_tag = product.find('div', class_='t4s-product-price')
        price_span = price_tag.find('span', class_='money') if price_tag else None
        product_price = price_span.text.strip() if price_span else 'Price not found'

        img_tag = product.find('img', class_='t4s-product-main-img')
        product_image = img_tag['src'] if img_tag and img_tag.has_attr('src') else None

        products.append({
            'name': product_name,
            'price': product_price,
            'url': product_url,
            'image': product_image
        })

        print(product_name, product_price, product_url, product_image)

    driver.quit()
    print(f"\nFound {len(products)} basketball shoes on Way of Wade")
    return products

def scrape_anta():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    url = 'https://anta.com/collections/anta-basketball?sort_by=manual&filter.v.t.shopify.target-gender=gid%3A%2F%2Fshopify%2FTaxonomyValue%2F19&filter.v.t.shopify.age-group=gid%3A%2F%2Fshopify%2FTaxonomyValue%2F2403&filter.p.m.custom.product_category=Shoes&filter.p.product_type=Basketball+Shoes&filter.v.price.gte=&filter.v.price.lte='
    driver.get(url)
    time.sleep(2)

    products = []

    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        product_cards = soup.find_all('div', class_='position-relative sm-full-screen-padding-x no-hidden pt-special-12')

        for product in product_cards:
            title_tag = product.find('p', class_='mb-1 title font-opposans-m')
            product_name = title_tag.text.strip() if title_tag else 'Name not found'

            category_tag = product.find('p', class_='mb-0 gender-information fs-small gray-500')
            if not category_tag or 'basketball shoes' not in category_tag.text.lower():
                continue

            sale_price_tag = product.find('span', class_='price-item--sale')
            regular_price_tag = product.find('span', class_='price-item--regular')
            if sale_price_tag:
                product_price = sale_price_tag.text.strip()
            elif regular_price_tag:
                product_price = regular_price_tag.text.strip()
            else:
                product_price = 'Price not found'

            url_tag = product.find('a', class_='stretched-link')
            product_url = url_tag['href'] if url_tag and url_tag.has_attr('href') else None
            if product_url and product_url.startswith('/'):
                product_url = 'https://anta.com' + product_url

            img_tag = product.find('img')
            product_image = img_tag['src'] if img_tag and img_tag.has_attr('src') else None

            products.append({
                'name': product_name,
                'price': product_price,
                'url': product_url,
                'image': product_image
            })

            print(product_name, product_price, product_url, product_image)

        try:
            next_page = driver.find_element(By.CSS_SELECTOR, 'a.as-pagination-link[aria-label="Next page"]')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_page)
            time.sleep(1)  # let it scroll
            driver.execute_script("arguments[0].click();", next_page)
            print("Clicked next page...")
            time.sleep(3)  # wait for next page to load
        except (NoSuchElementException, ElementNotInteractableException):
            print("No next page button found or can't click; finished scraping.")
            break

    driver.quit()
    print(f"\nFound {len(products)} basketball shoes on Anta")
    return products

def scrape_finishline():
    # TODO: implement GOAT scraper
    # Return list of dicts with keys: name, price, url, image
    return []

def scrape_footlocker():
    # TODO: implement GOAT scraper
    # Return list of dicts with keys: name, price, url, image
    return []

def scrape_eastbay():
    # TODO: implement GOAT scraper
    # Return list of dicts with keys: name, price, url, image
    return []

def scrape_dicks():
    # TODO: implement GOAT scraper
    # Return list of dicts with keys: name, price, url, image
    return []

def scrape_kohls():
    # TODO: implement GOAT scraper
    # Return list of dicts with keys: name, price, url, image
    return []

def scrape_champs():
    # TODO: implement GOAT scraper
    # Return list of dicts with keys: name, price, url, image
    return []

def scrape_zappos():
    # TODO: implement GOAT scraper
    # Return list of dicts with keys: name, price, url, image
    return []

def scrape_nba():
    # TODO: implement GOAT scraper
    # Return list of dicts with keys: name, price, url, image
    return []

def main():
    all_products = []

    print("Scraping Nike...")
    nike_products = scrape_nike()
    all_products.extend(nike_products)
    print(f"Got {len(nike_products)} products from Nike.\n")

    '''
    print("Scraping StockX...")
    stockx_products = scrape_stockx()
    all_products.extend(stockx_products)
    print(f"Got {len(stockx_products)} products from StockX.\n")
    '''

    '''
    print("Scraping GOAT...")
    goat_products = scrape_goat()
    all_products.extend(goat_products)
    print(f"Got {len(goat_products)} products from GOAT.\n")
    '''

    print("Scraping Under Armour...")
    ua_products = scrape_ua()
    all_products.extend(ua_products)
    print(f"Got {len(ua_products)} products from Under Armour.\n")

    print("Scraping Puma...")
    puma_products = scrape_puma()
    all_products.extend(puma_products)
    print(f"Got {len(puma_products)} products from Puma.\n")

    print("Scraping Way of Wade...")
    wayofwade_products = scrape_wayofwade()
    all_products.extend(wayofwade_products)
    print(f"Got {len(wayofwade_products)} products from Way of Wade.\n")

    print("Scraping Anta...")
    anta_products = scrape_anta()
    all_products.extend(anta_products)
    print(f"Got {len(anta_products)} products from Anta.\n")

    '''
    print("Scraping FinishLine...")
    finishline_products = scrape_finishline()
    all_products.extend(finishline_products)
    print(f"Got {len(finishline_products)} products from FinishLine.\n")
    '''

    '''
    print("Scraping FootLocker...")
    footlocker_products = scrape_footlocker()
    all_products.extend(footlocker_products)
    print(f"Got {len(footlocker_products)} products from FootLocker.\n")
    '''

    '''
    print("Scraping Eastbay...")
    eastbay_products = scrape_eastbay()
    all_products.extend(eastbay_products)
    print(f"Got {len(eastbay_products)} products from Eastbay.\n")
    '''

    '''
    print("Scraping Dick's Sporting Goods...")
    dicks_products = scrape_dicks()
    all_products.extend(dicks_products)
    print(f"Got {len(dicks_products)} products from Dick's Sporting Goods.\n")
    '''

    '''
    print("Scraping Kohl's...")
    kohls_products = scrape_kohls()
    all_products.extend(kohls_products)
    print(f"Got {len(kohls_products)} products from Kohl's.\n")
    '''

    '''
    print("Scraping Champs Sports...")
    champs_products = scrape_champs()
    all_products.extend(champs_products)
    print(f"Got {len(champs_products)} products from Champs Sports.\n")
    '''

    '''
    print("Scraping Zappos...")
    zappos_products = scrape_zappos()
    all_products.extend(zappos_products)
    print(f"Got {len(zappos_products)} products from Zappos.\n")
    '''

    '''
    print("Scraping NBA Store...")
    nba_products = scrape_nba()
    all_products.extend(nba_products)
    print(f"Got {len(nba_products)} products from NBA Store.\n")
    '''

    # Save as CSV
    with open('data/shoes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'price', 'url', 'image'])
        writer.writeheader()
        writer.writerows(all_products)
    print(f"\nSaved {len(all_products)} products to data/shoes.csv")

    # Save as JSON
    with open('data/shoes.json', 'w', encoding='utf-8') as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_products)} products to data/shoes.json")

    # Save to SQLite
    conn = sqlite3.connect('data/shoes.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS shoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            url TEXT,
            image TEXT
        )
    ''')

    # Clear old data
    c.execute('DELETE FROM shoes')

    # Insert new data
    c.executemany('''
        INSERT INTO shoes (name, price, url, image)
        VALUES (?, ?, ?, ?)
    ''', [(p['name'], p['price'], p['url'], p['image']) for p in all_products])

    conn.commit()
    conn.close()
    print(f"Saved {len(all_products)} products to data/shoes.db")

    # Use pandas
    df = pd.DataFrame(all_products)

    def clean_price(price_str):
        if not price_str:
            return None
        match = re.search(r'[\d,.]+', price_str)
        if match:
            return float(match.group(0).replace(',', ''))
        return None

    df['price_clean'] = df['price'].apply(clean_price)

    df = df[df['price_clean'].notnull()]

    max_price = df['price_clean'].max()
    bins = list(range(0, int(max_price) + 50, 50))
    labels = [f"${bins[i]}-${bins[i + 1] - 1}" for i in range(len(bins) - 1)]

    df['price_range'] = pd.cut(df['price_clean'], bins=bins, labels=labels, right=False)

    print("\nSample of data:")
    print(df.head())

    print("\nPrice range counts:")
    print(df['price_range'].value_counts().sort_index())

if __name__ == "__main__":
    main()
