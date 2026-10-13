# Book Scraper

A small Python command-line scraper that collects book data from [books.toscrape.com](https://books.toscrape.com), a practice website built for learning web scraping. It saves the results to a CSV file and prints a short summary.

## What it collects

For every book on each scraped page (20 books per page):

| Column | Description |
|---|---|
| `title` | Full book title (taken from the link's `title` attribute, since the visible text is shortened) |
| `price_gbp` | Price in British pounds, as a number |
| `rating` | Star rating from 1 to 5 |
| `in_stock` | `True` if the book is in stock, otherwise `False` |

## Requirements

- Python 3.9 or newer
- The `requests` and `beautifulsoup4` packages

Install the packages:

```bash
python -m pip install requests beautifulsoup4
```

## Usage

Run from the project folder:

```bash
python scrapper.py
```

Options:

| Option | Default | Description |
|---|---|---|
| `--pages` | `5` | Number of pages to scrape (the site has 50 in total) |
| `--output` | `books.csv` | Name of the CSV file to create |

Examples:

```bash
# Scrape the default 5 pages (100 books) into books.csv
python scrapper.py

# Scrape 10 pages into a custom file
python scrapper.py --pages 10 --output my_books.csv
```

## Example output

```
Scraping page 1/5...
Scraping page 2/5...
Scraping page 3/5...
Scraping page 4/5...
Scraping page 5/5...

Saved 100 books to books.csv

--- Summary ---
Total books     : 100
Average price   : £34.56
Cheapest book   : Patience (£10.16)
5-star books    : 19
```

## How it works

1. **Read options:** `argparse` reads `--pages` and `--output` from the command line.
2. **Download each page:** `fetch_page` builds the page URL (`.../catalogue/page-1.html`, `page-2.html`, ...) and downloads it with `requests`. It sends a User-Agent header and times out after 10 seconds. If a page fails, it prints an error and moves on to the next one.
3. **Parse the HTML:** `BeautifulSoup` turns the page into searchable elements. `parse_books` finds every book box (`article.product_pod`) and extracts the title, price, rating and stock status. The rating comes from a CSS class such as `star-rating Three`, which is converted to the number 3.
4. **Be polite:** the script waits 1 second between pages so it doesn't overload the server.
5. **Save and summarize:** `save_csv` writes all books to a CSV file, and `summarize` prints the total, average price, cheapest book and number of 5-star books.

## Project structure

```
SCRAPPER/
├── scrapper.py     # the scraper
├── books.csv       # output (created when you run it)
└── README.md
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'requests'`**: the packages aren't installed for the Python you are running. Use `python -m pip install requests beautifulsoup4`, so pip matches your Python.
- **`'python' is not recognized`**: Python isn't on your PATH. Reinstall Python and tick **"Add python.exe to PATH"** in the installer.
- **`Could not find platform independent libraries <prefix>`**: the Python installation is damaged. Repair or reinstall Python.
- **`Could not fetch page N`**: a network error or timeout. Check your internet connection and run again.

## Notes

- This site is designed for scraping practice. If you adapt the script to another website, check that site's terms of service and `robots.txt` first, and keep the delay between requests.
- Only the first 50 pages exist on this site, so use `--pages` values of 50 or less.
