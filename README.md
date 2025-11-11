# Travel Company Scraper

A Python web scraper to extract international travel company data from the Vietnamese National Tourism Administration website (quanlyluhanh.vn).

## Overview

This scraper collects information about all licensed international travel companies in Vietnam, including company names, addresses, licenses, contact details, and business scope.

**Website:** https://quanlyluhanh.vn/index.php/cat/1001  
**Total Pages:** 478  
**Total Companies:** ~4,775

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Command Line Usage

```bash
# Scrape first 10 pages and save to CSV
python main.py --start-page 1 --end-page 10 --output companies.csv

# Scrape specific pages and save as JSON
python main.py --start-page 1 --end-page 5 --output companies.json --format json

# Scrape all 478 pages (takes ~8-10 minutes)
python main.py --start-page 1 --end-page 478 --output all_companies.csv

# Or use the dedicated script for full scrape
python scrape_all.py
```

### Python API Usage

```python
from scraper import TravelCompanyScraper

# Create scraper instance with 1 second delay between requests
scraper = TravelCompanyScraper(delay=1.0)

# Scrape a single page
companies = scraper.scrape_page(1)

# Scrape a range of pages
companies = scraper.scrape_all_pages(start_page=1, end_page=10)

# Save to CSV
scraper.save_to_csv(companies, 'travel_companies.csv')

# Save to JSON
scraper.save_to_json(companies, 'travel_companies.json')
```

See `example.py` for more usage examples.

## Command Line Options

```
-o, --output        Output filename (default: travel_companies.csv)
-f, --format        Output format: csv or json (default: csv)
-s, --start-page    Starting page number (default: 1)
-e, --end-page      Ending page number (default: scrape all pages)
-d, --delay         Delay between requests in seconds (default: 1.0)
-v, --verbose       Enable verbose logging
```

## Data Fields

Each company record includes:

| Field | Description |
|-------|-------------|
| `vietnamese_name` | Company name in Vietnamese |
| `english_name` | Company name in English |
| `address` | Business address |
| `license_number` | Tourism business license number |
| `issue_date` | License issue date |
| `phone` | Contact phone number |
| `website` | Company website URL |
| `email` | Contact email address |
| `business_scope` | Business activities (Inbound, Outbound, Domestic) |
| `source_page` | URL of the source page |

## Features

✅ Scrapes all international travel company data  
✅ Multi-page support with pagination (478 pages)  
✅ Export to CSV or JSON format  
✅ Configurable rate limiting (respectful scraping)  
✅ Comprehensive error handling  
✅ Progress logging  
✅ UTF-8 encoding support for Vietnamese text  

## Rate Limiting

The scraper includes built-in rate limiting to be respectful to the server:
- Default delay: 1.0 second between requests
- Configurable via `delay` parameter
- Recommended: 0.7-1.5 seconds for full scrapes

## Examples

### Scrape First Page Only
```bash
python main.py --start-page 1 --end-page 1 --output test.csv
```

### Scrape All Data
```bash
python scrape_all.py
```

### Custom Delay
```bash
python main.py --delay 1.5 --start-page 1 --end-page 100 --output companies.csv
```

## Output Format

### CSV Example
```csv
vietnamese_name,english_name,address,license_number,issue_date,phone,website,email,business_scope,source_page
CÔNG TY TNHH THƯƠNG MẠI VÀ DU LỊCH QUỐC TẾ TRUST TRAVEL,TRUST TRAVEL INTERNATIONAL TRADE AND TRAVEL COMPANY LIMITED,"SỐ 19, NGÁCH 20/82/2 ĐƯỜNG PHÚ MINH",01-3012/2025/CDLQGVN-GP LHQT,12/11/2025,0342540868,https://trusttravel.vn/,contact@trusttravel.vn,"Inbound, Nội địa",https://quanlyluhanh.vn/index.php/cat/1001
```

### JSON Example
```json
[
  {
    "vietnamese_name": "CÔNG TY TNHH THƯƠNG MẠI VÀ DU LỊCH QUỐC TẾ TRUST TRAVEL",
    "english_name": "TRUST TRAVEL INTERNATIONAL TRADE AND TRAVEL COMPANY LIMITED",
    "address": "SỐ 19, NGÁCH 20/82/2 ĐƯỜNG PHÚ MINH",
    "license_number": "01-3012/2025/CDLQGVN-GP LHQT",
    "issue_date": "12/11/2025",
    "phone": "0342540868",
    "website": "https://trusttravel.vn/",
    "email": "contact@trusttravel.vn",
    "business_scope": "Inbound, Nội địa",
    "source_page": "https://quanlyluhanh.vn/index.php/cat/1001"
  }
]
```

## Project Structure

```
travel-scraper/
├── scraper/
│   ├── __init__.py
│   └── travel_scraper.py    # Main scraper class
├── main.py                   # CLI interface
├── example.py                # Usage examples
├── scrape_all.py            # Full scrape script
├── requirements.txt          # Dependencies
├── README.md                # This file
└── .gitignore
```

## License

This project is for educational and research purposes only. Please respect the website's terms of service and use responsibly.
