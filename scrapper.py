from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def fetch_autoria_listings():
    url = (
        "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search"
    )

    options = Options()
    # Можно закомментировать, чтобы видеть браузер
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)  # ждём загрузки JS

    html = driver.page_source
    driver.quit()
    return html

def parse_listings(html):
    soup = BeautifulSoup(html, "html.parser")
    listings = []

    cars = soup.select(".ticket-item")
    print("Найдено элементов:", len(cars))

    for car in cars:
        title_tag = car.select_one(".address")
        price_tag = car.select_one(".price-ticket")
        link_tag = car.select_one(".m-link-ticket")

        title = title_tag.get_text(strip=True) if title_tag else "Без назви"
        price = price_tag.get_text(strip=True) if price_tag else "Невідома ціна"
        link = link_tag["href"] if link_tag else "Немає посилання"

        listings.append({
            "title": title,
            "price": price,
            "link": link
        })

    return listings
