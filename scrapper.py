import argparse
import csv
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
HEADERS = {"User-Agent": "Mozilla/5.0 (student-project scraper)"}


def fetch_page(page_number):
    """Download one page, return parsed HTML or None on failure."""
    url = BASE_URL.format(page_number)
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  Could not fetch page {page_number}: {e}")
        return None
    return BeautifulSoup(response.text, "html.parser")


def parse_books(soup):
    """Extract book data from one parsed page."""
    books = []
    for item in soup.select("article.product_pod"):
        title = item.h3.a["title"]
        price = float(item.select_one("p.price_color").text.replace("£", "").replace("Â", ""))
        rating_word = item.select_one("p.star-rating")["class"][1]
        in_stock = "In stock" in item.select_one("p.availability").text
        books.append({
            "title": title,
            "price_gbp": price,
            "rating": RATING_MAP.get(rating_word, 0),
            "in_stock": in_stock,
        })
    return books


def save_csv(books, filename="books.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price_gbp", "rating", "in_stock"])
        writer.writeheader()
        writer.writerows(books)
    print(f"\nSaved {len(books)} books to {filename}")


def summarize(books):
    if not books:
        return
    avg_price = sum(b["price_gbp"] for b in books) / len(books)
    cheapest = min(books, key=lambda b: b["price_gbp"])
    top_rated = [b for b in books if b["rating"] == 5]
    print("\n--- Summary ---")
    print(f"Total books     : {len(books)}")
    print(f"Average price   : £{avg_price:.2f}")
    print(f"Cheapest book   : {cheapest['title']} (£{cheapest['price_gbp']})")
    print(f"5-star books    : {len(top_rated)}")


def main():
    parser = argparse.ArgumentParser(description="Scrape books.toscrape.com into a CSV")
    parser.add_argument("--pages", type=int, default=5, help="number of pages to scrape (max 50)")
    parser.add_argument("--output", default="books.csv")
    args = parser.parse_args()

    all_books = []
    for page in range(1, args.pages + 1):
        print(f"Scraping page {page}/{args.pages}...")
        soup = fetch_page(page)
        if soup is None:
            continue
        all_books.extend(parse_books(soup))
        time.sleep(1)  # be polite to the server

    save_csv(all_books, args.output)
    summarize(all_books)


if __name__ == "__main__":
    main()