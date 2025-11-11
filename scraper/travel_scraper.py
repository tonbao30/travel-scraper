"""
Travel Company Scraper for quanlyluhanh.vn
Scrapes international travel company data from Vietnamese tourism authority website
"""

import requests
from bs4 import BeautifulSoup
import time
import re
import json
import csv
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TravelCompanyScraper:
    """Scraper for travel company data from quanlyluhanh.vn"""
    
    BASE_URL = "https://quanlyluhanh.vn/index.php/cat/1001"
    
    def __init__(self, delay: float = 1.0):
        """
        Initialize the scraper
        
        Args:
            delay: Delay between requests in seconds (default: 1.0)
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_page(self, page_num: int = 1) -> List[Dict[str, str]]:
        """
        Scrape a single page of company data
        
        Args:
            page_num: Page number to scrape (default: 1)
            
        Returns:
            List of company dictionaries
        """
        if page_num == 1:
            url = self.BASE_URL
        else:
            url = f"{self.BASE_URL}/{page_num}"
        
        logger.info(f"Scraping page {page_num}: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all company name blocks
            name_blocks = soup.find_all('div', class_='company-name')
            
            companies = []
            
            for name_block in name_blocks:
                try:
                    # Get Vietnamese and English names
                    vn_name_div = name_block.find('div', class_='tendn')
                    en_name_div = name_block.find('div', class_='tengiaodich')
                    
                    vn_name = ""
                    en_name = ""
                    
                    if vn_name_div:
                        vn_text = vn_name_div.get_text(strip=True)
                        # Remove the number prefix like "1. Tên tiếng Việt: "
                        vn_name = re.sub(r'^\d+\.\s*Tên tiếng Việt:\s*', '', vn_text, flags=re.IGNORECASE).strip()
                    
                    if en_name_div:
                        en_text = en_name_div.get_text(strip=True)
                        en_name = re.sub(r'^Tên tiếng Anh:\s*', '', en_text, flags=re.IGNORECASE).strip()
                    
                    # Find the next sibling with thick-border class for other info
                    info_block = name_block.find_next_sibling('div', class_='thick-border')
                    
                    company_data = {
                        'vietnamese_name': vn_name,
                        'english_name': en_name,
                        'address': '',
                        'license_number': '',
                        'issue_date': '',
                        'phone': '',
                        'website': '',
                        'email': '',
                        'business_scope': '',
                        'source_page': url
                    }
                    
                    if info_block:
                        # Find all li elements with class 'info'
                        info_items = info_block.find_all('li', class_='info')
                        
                        field_mapping = {
                            "Địa chỉ": "address",
                            "Giấy phép kinh doanh lữ hành số": "license_number",
                            "Giấy phép": "license_number",
                            "Ngày cấp": "issue_date",
                            "Điện thoại": "phone",
                            "Website": "website",
                            "Email": "email",
                            "Phạm vi hoạt động": "business_scope"
                        }
                        
                        for item in info_items:
                            item_text = item.get_text(strip=True)
                            for vn_field, key in field_mapping.items():
                                if item_text.startswith(vn_field + ":"):
                                    value = item_text.replace(vn_field + ":", "").strip()
                                    if value and not company_data[key]:
                                        company_data[key] = value
                                    break
                    
                    # Clean website URL
                    if company_data['website']:
                        website = company_data['website']
                        if not website.startswith('http'):
                            if website.startswith('www.'):
                                company_data['website'] = 'https://' + website
                            else:
                                company_data['website'] = 'https://' + website
                    
                    # Only add if we have at least a company name
                    if company_data['vietnamese_name'] or company_data['english_name']:
                        companies.append(company_data)
                        logger.debug(f"Parsed company: {company_data.get('vietnamese_name', 'N/A')}")
                
                except Exception as e:
                    logger.error(f"Error parsing company block: {e}")
                    continue
            
            logger.info(f"Found {len(companies)} companies on page {page_num}")
            return companies
            
        except requests.RequestException as e:
            logger.error(f"Error fetching page {page_num}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error on page {page_num}: {e}")
            return []
    
    def get_total_pages(self) -> int:
        """
        Get the total number of pages
        
        Returns:
            Total number of pages
        """
        try:
            response = self.session.get(self.BASE_URL, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Look for pagination links
            # Pattern: "Cuối cùng" link or highest numbered page
            pagination = soup.find_all('a', href=re.compile(r'/cat/1001/\d+'))
            
            max_page = 1
            for link in pagination:
                href = link.get('href', '')
                page_match = re.search(r'/cat/1001/(\d+)', href)
                if page_match:
                    page_num = int(page_match.group(1))
                    max_page = max(max_page, page_num)
            
            logger.info(f"Total pages detected: {max_page}")
            return max_page
            
        except Exception as e:
            logger.error(f"Error getting total pages: {e}")
            return 1
    
    def scrape_all_pages(self, start_page: int = 1, end_page: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Scrape all pages or a range of pages
        
        Args:
            start_page: Starting page number (default: 1)
            end_page: Ending page number (default: None, will scrape all pages)
            
        Returns:
            List of all company dictionaries
        """
        if end_page is None:
            end_page = self.get_total_pages()
        
        all_companies = []
        
        for page_num in range(start_page, end_page + 1):
            companies = self.scrape_page(page_num)
            all_companies.extend(companies)
            
            # Respect rate limiting
            if page_num < end_page:
                time.sleep(self.delay)
        
        logger.info(f"Total companies scraped: {len(all_companies)}")
        return all_companies
    
    def save_to_csv(self, companies: List[Dict[str, str]], filename: str) -> None:
        """
        Save company data to CSV file
        
        Args:
            companies: List of company dictionaries
            filename: Output CSV filename
        """
        if not companies:
            logger.warning("No companies to save")
            return
        
        fieldnames = [
            'vietnamese_name', 'english_name', 'address', 
            'license_number', 'issue_date', 'phone', 'website', 
            'email', 'business_scope', 'source_page'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(companies)
            
            logger.info(f"Saved {len(companies)} companies to {filename}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    def save_to_json(self, companies: List[Dict[str, str]], filename: str) -> None:
        """
        Save company data to JSON file
        
        Args:
            companies: List of company dictionaries
            filename: Output JSON filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(companies, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(companies)} companies to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
