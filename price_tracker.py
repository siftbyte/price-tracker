import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0"}
CSV_FILE = "prices.csv"

PRODUCTS = [
    {
        "name": "PS5 Digital Slim (Datart)",
        "url": "https://www.datart.cz/herni-konzole-sony-playstation-5-digital-typ-modelu-slim-ps711000049751-bila",
    },
    {
        "name": "PS5 Digital Slim Blu-ray (Datart)",
        "url": "https://www.datart.cz/herni-konzole-sony-playstation-5-typ-modelu-slim-ps711000049742-bila",
    }
]


def get_price(url):
    """Download the product page and return the price as an integer."""
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    price_element = soup.find("div", class_="actual")
    text = price_element.get_text()

    digits = ""
    for char in text:
        if char.isdigit():
            digits = digits + char

    return int(digits)


def get_last_price(product_name):
    """Return the last saved price of the product, or None if there is none."""
    try:
        with open(CSV_FILE, encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return None

    last_price = None
    for line in lines:
        date, name, price = line.strip().split(",")
        if name == product_name:
            last_price = int(price)
    return last_price


def save_price(product_name, price):
    """Append the current price to the CSV file."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(CSV_FILE, "a", encoding="utf-8") as file:
        file.write(f"{now},{product_name},{price}\n")


def main():
    for product in PRODUCTS:
        name = product["name"]
        price = get_price(product["url"])
        last_price = get_last_price(name)

        print(f"{name}: {price} CZK")

        if last_price is None:
            print("  First measurement, nothing to compare.")
        elif price < last_price:
            print(f"  Price dropped by {last_price - price} CZK!")
        elif price > last_price:
            print(f"  Price increased by {price - last_price} CZK.")
        else:
            print("  Price unchanged.")

        save_price(name, price)


if __name__ == "__main__":
    main()