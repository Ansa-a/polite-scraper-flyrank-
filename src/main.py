import os
import requests

URL = "https://books.toscrape.com/catalogue/page-1.html"
CACHE_FILE = "cache/catalogue-page-1.html"
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/Ansa-a)"

def fetch_catalogue_page():
    # Ensure cache directory exists
    os.makedirs("cache", exist_ok=True)

    # Check if cached version already exists
    if os.path.exists(CACHE_FILE):
        file_size = os.path.getsize(CACHE_FILE)
        print(f"CACHE HIT: Read from {CACHE_FILE} (Size: {file_size} bytes)")
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return f.read()

    # Otherwise, fetch from the web politely
    print(f"FETCH: Downloading from {URL}")
    headers = {"User-Agent": USER_AGENT}
    
    try:
        response = requests.get(URL, headers=headers, timeout=5)
        
        # Check status code
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return None
        
        html_content = response.text
        
        # Save to cache
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"SUCCESS: Cached page saved (Size: {len(html_content)} bytes)")
        return html_content

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    fetch_catalogue_page()