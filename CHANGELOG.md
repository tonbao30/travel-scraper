# Changelog

## [1.0.0] - 2025-11-11

### Initial Release

#### Added
- Complete web scraper for quanlyluhanh.vn international travel companies
- `TravelCompanyScraper` class with full scraping functionality
- Command-line interface (main.py) with argparse support
- Export functionality to CSV and JSON formats
- Multi-page scraping with pagination support (478 pages)
- Configurable rate limiting between requests
- Comprehensive error handling and logging
- UTF-8 encoding support for Vietnamese text
- Example usage scripts (example.py, scrape_all.py)
- Full documentation in README.md

#### Features
- Scrapes 10 data fields per company:
  - Vietnamese and English names
  - Address
  - License number and issue date
  - Phone, email, website
  - Business scope
  - Source page URL
- HTML parsing using BeautifulSoup4 with lxml parser
- Respectful scraping with delay configuration
- Progress logging with Python logging module
- Session management with requests library

#### Technical Details
- Python 3.7+ compatible
- Dependencies: requests, beautifulsoup4, lxml, pandas
- Tested on Windows with PowerShell and CMD
- Successfully tested with multiple page ranges
- Validated output in both CSV and JSON formats

#### Known Limitations
- Requires internet connection
- Depends on website HTML structure (may break if website updates)
- No resume capability for interrupted scrapes (planned for future)
- No built-in data validation/cleaning (outputs raw data)

### Testing Summary
- ✅ Single page scraping (10 companies)
- ✅ Multiple page scraping (30 companies from 3 pages)
- ✅ CSV export with UTF-8 BOM encoding
- ✅ JSON export with proper Unicode handling
- ✅ Command-line interface with all options
- ✅ Python API usage
- ✅ Example scripts execution
