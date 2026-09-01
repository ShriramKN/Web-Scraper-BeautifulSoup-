import os
import csv
import json
import time
import random
import logging
import sqlite3
import argparse
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
import concurrent.futures

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==========================================
# WEB SCRAPER CLASS
# ==========================================
class AdvancedWebScraper:
    """
    A robust, object-oriented Web Scraper utilizing BeautifulSoup.
    Features include robots.txt parsing, user-agent rotation, retries, and data export.
    """

    def __init__(self, base_url: str, delay: float = 1.5, max_retries: int = 3, respect_robots: bool = True):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.delay = delay
        self.max_retries = max_retries
        self.respect_robots = respect_robots
        self.scraped_data: List[Dict[str, Any]] = []
        
        # Setup session for connection pooling
        self.session = requests.Session()
        
        # Parse robots.txt if required
        self.robot_parser = None
        if self.respect_robots:
            self._init_robots_txt()

    def _init_robots_txt(self) -> None:
        """Fetches and parses the robots.txt file for the domain."""
        robots_url = urljoin(self.base_url, "/robots.txt")
        self.robot_parser = RobotFileParser()
        self.robot_parser.set_url(robots_url)
        try:
            self.robot_parser.read()
            logger.info(f"Successfully loaded robots.txt from {robots_url}")
        except Exception as e:
            logger.warning(f"Could not load robots.txt: {e}")
            self.robot_parser = None

    def _can_fetch(self, url: str, user_agent: str) -> bool:
        """Checks if scraping the URL is allowed by robots.txt."""
        if not self.respect_robots or not self.robot_parser:
            return True
        return self.robot_parser.can_fetch(user_agent, url)

    def _get_random_headers(self) -> Dict[str, str]:
        """Generates random headers to mimic a real browser."""
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/"
        }

    def fetch_page(self, url: str) -> Optional[str]:
        """Fetches the HTML content of a URL with retries and exponential backoff."""
        headers = self._get_random_headers()
        
        if not self._can_fetch(url, headers["User-Agent"]):
            logger.warning(f"Robots.txt restricts scraping for URL: {url}")
            return None

        for attempt in range(1, self.max_retries + 1):
            try:
                # Politeness delay
                time.sleep(self.delay + random.uniform(0.5, 1.5))
                
                logger.info(f"Fetching [Attempt {attempt}/{self.max_retries}]: {url}")
                response = self.session.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                return response.text
                
            except RequestException as e:
                logger.error(f"Error fetching {url}: {e}")
                if attempt < self.max_retries:
                    sleep_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    logger.error(f"Max retries reached for {url}. Skipping.")
                    return None

    # --- HTML PARSING METHODS ---

    def parse_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extracts standard SEO metadata like title, description, and keywords."""
        metadata = {}
        
        title_tag = soup.find('title')
        metadata['title'] = title_tag.get_text(strip=True) if title_tag else ""
        
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        metadata['description'] = desc_tag['content'] if desc_tag and 'content' in desc_tag.attrs else ""
        
        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        metadata['keywords'] = keywords_tag['content'] if keywords_tag and 'content' in keywords_tag.attrs else ""
        
        return metadata

    def parse_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """Extracts and resolves all unique internal and external links."""
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(current_url, href)
            # Remove URL fragments
            full_url = full_url.split('#')[0]
            if full_url.startswith('http'):
                links.add(full_url)
        return list(links)

    def parse_tables(self, soup: BeautifulSoup) -> List[List[Dict[str, str]]]:
        """Extracts HTML tables and converts them to a list of dictionaries."""
        all_tables_data = []
        for table in soup.find_all('table'):
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            rows = table.find_all('tr')
            
            table_data = []
            for row in rows:
                cells = row.find_all('td')
                if cells:
                    # Map headers to cell values, default to 'Col_X' if no header
                    row_data = {}
                    for i, cell in enumerate(cells):
                        key = headers[i] if i < len(headers) else f"Col_{i}"
                        row_data[key] = cell.get_text(strip=True)
                    table_data.append(row_data)
                    
            if table_data:
                all_tables_data.append(table_data)
                
        return all_tables_data

    def process_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Main method to process a single URL and extract all desired data."""
        html = self.fetch_page(url)
        if not html:
            return None
            
        soup = BeautifulSoup(html, 'html.parser')
        
        data = {
            'url': url,
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'metadata': self.parse_metadata(soup),
            'links_found': len(self.parse_links(soup, url)),
            'tables_found': self.parse_tables(soup)
        }
        
        logger.info(f"Successfully parsed data from {url}")
        return data

    def crawl_concurrently(self, urls: List[str], max_workers: int = 3) -> None:
        """Uses threads to scrape multiple URLs concurrently."""
        logger.info(f"Starting concurrent crawl of {len(urls)} URLs with {max_workers} workers.")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_url = {executor.submit(self.process_url, url): url for url in urls}
            
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    if data:
                        self.scraped_data.append(data)
                except Exception as e:
                    logger.error(f"Thread execution failed for {url}: {e}")

    # --- DATA EXPORT METHODS ---

    def export_to_json(self, filename: str = "output.json") -> None:
        """Saves scraped data to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=4, ensure_ascii=False)
        logger.info(f"Data exported to JSON: {filename}")

    def export_to_csv(self, filename: str = "output.csv") -> None:
        """Saves basic metadata to a CSV file."""
        if not self.scraped_data:
            logger.warning("No data to export to CSV.")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['URL', 'Title', 'Description', 'Scraped At', 'Links Found', 'Tables Found'])
            
            for item in self.scraped_data:
                writer.writerow([
                    item.get('url'),
                    item.get('metadata', {}).get('title', ''),
                    item.get('metadata', {}).get('description', ''),
                    item.get('scraped_at'),
                    item.get('links_found'),
                    len(item.get('tables_found', []))
                ])
        logger.info(f"Data exported to CSV: {filename}")

    def export_to_sqlite(self, db_name: str = "scraper.db") -> None:
        """Saves scraped data into a local SQLite database."""
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            
            # Create table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    title TEXT,
                    description TEXT,
                    scraped_at TEXT,
                    links_count INTEGER
                )
            ''')
            
            # Insert data
            for item in self.scraped_data:
                cursor.execute('''
                    INSERT OR REPLACE INTO pages (url, title, description, scraped_at, links_count)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    item.get('url'),
                    item.get('metadata', {}).get('title', ''),
                    item.get('metadata', {}).get('description', ''),
                    item.get('scraped_at'),
                    item.get('links_found')
                ))
                
            conn.commit()
            conn.close()
            logger.info(f"Data exported to SQLite DB: {db_name}")
            
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")

# ==========================================
# MAIN EXECUTION BLOCK
# ==========================================
if __name__ == "__main__":
    # Setup Command Line Interface
    parser = argparse.ArgumentParser(description="Advanced Python Web Scraper using BeautifulSoup")
    parser.add_argument('-u', '--urls', nargs='+', required=True, help="List of URLs to scrape")
    parser.add_argument('-w', '--workers', type=int, default=3, help="Number of concurrent threads")
    parser.add_argument('--no-robots', action='store_true', help="Ignore robots.txt (Not recommended)")
    
    args = parser.parse_args()

    # Determine base URL from the first URL provided
    primary_url = args.urls[0]
    
    # Initialize the Scraper
    scraper = AdvancedWebScraper(
        base_url=primary_url,
        delay=2.0,
        max_retries=3,
        respect_robots=not args.no_robots
    )
    
    # Start crawling
    print("\n" + "="*50)
    print("🚀 Starting Advanced Web Scraper...")
    print("="*50 + "\n")
    
    start_time = time.time()
    
    # If multiple URLs, use concurrent crawling. If single, use simple processing.
    if len(args.urls) > 1:
        scraper.crawl_concurrently(args.urls, max_workers=args.workers)
    else:
        result = scraper.process_url(primary_url)
        if result:
            scraper.scraped_data.append(result)
            
    # Export Phase
    if scraper.scraped_data:
        print("\n💾 Exporting Data...")
        scraper.export_to_json("scraped_results.json")
        scraper.export_to_csv("scraped_results.csv")
        scraper.export_to_sqlite("scraped_results.db")
    else:
        print("\n⚠️ No data was scraped successfully.")
        
    elapsed_time = time.time() - start_time
    print(f"\n✅ Scraping complete in {elapsed_time:.2f} seconds.")
    print(f"Total pages scraped: {len(scraper.scraped_data)}")
