from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import random

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
    time.sleep(2)  # let page start loading
    # wait_manual_bypass(30)

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

    # Scroll to load all products
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

    # Find all product tiles
    product_links = soup.find_all('a', attrs={'data-test-id': 'product-list-item-link'})

    products = []

    for link in product_links:
        # Name
        name_tag = link.find('h3')
        product_name = name_tag.text.strip() if name_tag else 'Name not found'

        # URL
        href = link.get('href')
        product_url = 'https://us.puma.com' + href if href else None

        # Image
        image_tag = link.find('img')
        product_image = image_tag['src'] if image_tag and image_tag.has_attr('src') else None

        # Price: try sale price first, then regular price
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

    url = 'https://wayofwade.com/collections/basketball-shoes'  # replace with actual basketball page if different
    driver.get(url)
    time.sleep(2)

    # Scroll to load all products
    SCROLL_PAUSE_TIME = 2
    max_attempts_without_new = 5
    attempts = 0

    last_height = driver.execute_script("return document.body.scrollHeight")

    while attempts < max_attempts_without_new:
        # Scroll to ~90% of the page to trigger lazy load
        driver.execute_script("""
            window.scrollTo(0, document.body.scrollHeight * 0.9);
        """)
        time.sleep(SCROLL_PAUSE_TIME)

        # Then scroll to bottom to load last items
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

    # Each product container
    product_divs = soup.find_all('div', class_='t4s-product')

    for product in product_divs:
        # Name & URL
        name_tag = product.find('h3', class_='t4s-product-title')
        url_tag = name_tag.find('a') if name_tag else None

        product_name = name_tag.text.strip() if name_tag else 'Name not found'

        if 'slide' in product_name.lower():
            continue

        product_url = url_tag['href'] if url_tag and url_tag.has_attr('href') else None
        if product_url and product_url.startswith('/'):
            product_url = 'https://wayofwade.com' + product_url

        # Price
        price_tag = product.find('div', class_='t4s-product-price')
        price_span = price_tag.find('span', class_='money') if price_tag else None
        product_price = price_span.text.strip() if price_span else 'Price not found'

        # Image
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
    # TODO: implement GOAT scraper
    # Return list of dicts with keys: name, price, url, image
    return []

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

    '''
    print("Scraping Anta...")
    anta_products = scrape_anta()
    all_products.extend(anta_products)
    print(f"Got {len(anta_products)} products from Anta.\n")
    '''

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

    # Save combined results
    with open('data/shoes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'price', 'url', 'image'])
        writer.writeheader()
        writer.writerows(all_products)
    print(f"\nSaved total {len(all_products)} products to data/shoes.csv")

if __name__ == "__main__":
    main()
