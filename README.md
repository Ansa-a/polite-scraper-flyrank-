# Polite Web Scraper & Catalog Extraction Pipeline

A robust, polite, and production-grade Python web scraper engineered to extract bibliographic data from [Books to Scrape](https://books.toscrape.com/). Built with built-in caching, strict rate-limiting, schema validation, and comprehensive run reporting.

---

## Features

- **Polite Scraping Architecture**: Enforces a mandatory delay between requests, includes a custom identifying `User-Agent`, and implements graceful timeout and error handling.
- **Local Caching Layer**: Caches raw HTML responses locally to minimize redundant network calls during development and testing.
- **Dynamic Pagination**: Automatically traverses catalog pages from start to finish without hardcoded limits.
- **Data Validation & Error Resilience**: Validates extracted records against strict schemas, routing invalid items or broken URLs to an error log (`errors.json`) while keeping the main pipeline running.
- **Structured JSON & CSV Output**: Exports clean, deduplicated datasets alongside execution summaries (`run-report.json`).

---

## Project Structure

```text
politescrapper/
├── cache/                  # Local HTML cache directory
├── output/                 # Generated datasets and reports (books.json, errors.json, run-report.json)
├── src/                    # Source code module
│   └── main.py             # Main execution script
├── README.md               # Project documentation
└── requirements.txt        # Project dependencies

**Setup & Installation**
1 Clone the repository:
Bash
git clone [https://github.com/Ansa-a/politescrapper.git](https://github.com/Ansa-a/politescrapper.git)
cd politescrapper

2 Create and activate a virtual environment:
Bash
python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

3 Install dependencies:
Bash
pip install -r requirements.txt
Running the Pipeline

4 Execute the main script from the root directory:
Bash
python src/main.py