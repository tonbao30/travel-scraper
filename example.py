"""
Example script demonstrating how to use the TravelCompanyScraper
"""

from scraper import TravelCompanyScraper

# Example 1: Scrape first 5 pages and save to CSV
print("Example 1: Scraping first 5 pages...")
scraper = TravelCompanyScraper(delay=1.0)
companies = scraper.scrape_all_pages(start_page=1, end_page=5)
scraper.save_to_csv(companies, 'example_companies.csv')
print(f"✓ Saved {len(companies)} companies to example_companies.csv\n")

# Example 2: Scrape a single page
print("Example 2: Scraping page 10...")
scraper = TravelCompanyScraper()
companies_page_10 = scraper.scrape_page(10)
print(f"✓ Found {len(companies_page_10)} companies on page 10\n")

# Example 3: Display first company details
if companies_page_10:
    print("Example 3: First company details from page 10:")
    company = companies_page_10[0]
    print(f"  Vietnamese Name: {company['vietnamese_name']}")
    print(f"  English Name: {company['english_name']}")
    print(f"  Address: {company['address']}")
    print(f"  Phone: {company['phone']}")
    print(f"  Email: {company['email']}")
    print(f"  Website: {company['website']}")
    print(f"  License: {company['license_number']}")
    print(f"  Issue Date: {company['issue_date']}")
    print(f"  Business Scope: {company['business_scope']}\n")

# Example 4: Save to JSON
print("Example 4: Saving to JSON...")
scraper.save_to_json(companies_page_10, 'example_page_10.json')
print(f"✓ Saved to example_page_10.json\n")

print("All examples completed successfully!")
