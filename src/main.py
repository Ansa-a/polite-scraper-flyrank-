import csv
import os
import time
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/Ansa-a)"


def fetch_and_cache_page(url, filename):
  """Fetches a page politely with caching, rate limiting, and error handling."""
  os.makedirs("cache", exist_ok=True)

  # Check local cache first
  if os.path.exists(filename):
    file_size = os.path.getsize(filename)
    print(f"CACHE HIT: Read from {filename} (Size: {file_size} bytes)")
    with open(filename, "r", encoding="utf-8") as f:
      return f.read()

  # Enforce politeness rate-limiting delay before live request (at least 500ms)
  print(f"WAIT: Sleeping for 0.5 seconds before request...")
  time.sleep(0.5)

  print(f"FETCH: Downloading from {url}")
  headers = {"User-Agent": USER_AGENT}

  try:
    response = requests.get(url, headers=headers, timeout=5)
    if response.status_code != 200:
      print(f"Error: Received status code {response.status_code}")
      return None

    html_content = response.text

    # Save to local cache
    with open(filename, "w", encoding="utf-8") as f:
      f.write(html_content)

    print(f"SUCCESS: Cached page saved to {filename}")
    return html_content

  except requests.exceptions.Timeout:
    print("Error: Request timed out.")
    return None
  except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    return None


def extract_book_data(book):
  """Extracts title, price, availability, and rating from a single book pod."""
  title = book.h3.find("a")["title"]
  price = book.select_one("p.price_color").text
  availability = book.select_one("p.instock.availability").text.strip()
  rating_classes = book.select_one("p.star-rating")["class"]
  rating = rating_classes[1]

  return {
      "title": title,
      "price": price,
      "availability": availability,
      "rating": rating,
  }


def save_books_to_csv(books_list, filename="books_output.csv"):
  """Saves a list of book dictionaries to a CSV file using utf-8-sig."""
  fieldnames = ["title", "price", "availability", "rating"]

  with open(filename, mode="w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for book in books_list:
      writer.writerow(book)

  print(f"\nSUCCESS: Saved {len(books_list)} books to {filename}")


def scrape_all_pages():
  """Dynamically discovers and scrapes all pages until no 'next' link remains."""
  current_url = START_URL
  all_books = []
  page_num = 1

  while current_url:
    cache_filename = f"cache/catalogue-page-{page_num}.html"
    print(f"\n--- Processing Page {page_num}: {current_url} ---")

    html_content = fetch_and_cache_page(current_url, cache_filename)
    if not html_content:
      print(f"Failed to retrieve page {page_num}. Stopping.")
      break

    # Parse and extract books
    soup = BeautifulSoup(html_content, "html.parser")
    books = soup.select("article.product_pod")
    print(f"Found {len(books)} books on this page.")

    for book in books:
      book_data = extract_book_data(book)
      all_books.append(book_data)

    # Find the 'next' button for the subsequent page
    next_button = soup.select_one("li.next > a")

    if next_button and next_button.get("href"):
      next_href = next_button["href"]
      current_url = BASE_URL + next_href
      page_num += 1
    else:
      print("\nNo more 'next' pages found. Reached the end of the catalog!")
      current_url = None  # This exits the while loop gracefully

  # Save the massive collection of all books across all pages
  save_books_to_csv(all_books, filename="all_books_output.csv")


if __name__ == "__main__":
  scrape_all_pages()