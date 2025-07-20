from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def main():
    # Setup ChromeDriver automatically
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    url = 'https://www.nike.com/w/mens-basketball-shoes-3glsmznik1zy7ok'
    driver.get(url)

    # Scroll to the bottom to load all products
    SCROLL_PAUSE_TIME = 2

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Check if we've reached the bottom
        if new_height == last_height:
            break
        last_height = new_height

    # Get page source after JS loads
    html = driver.page_source

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    container = soup.find('div', id='skip-to-products')
    shoes = container.find_all('div', attrs={'data-product-position': True})

    for shoe in shoes:
        name_tag = shoe.find('a', class_='product-card__link-overlay')
        price_tag = shoe.find('div', class_='product-price')

        if name_tag and price_tag:
            product_name = name_tag.text.strip()
            product_price = price_tag.text.strip()
            print(product_name, product_price)

    driver.quit()

if __name__ == "__main__":
    main()
