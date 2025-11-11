"""
Full scraping script to get all companies from all 478 pages
WARNING: This will take approximately 8-10 minutes to complete
"""

from scraper import TravelCompanyScraper
import time

def main():
    print("=" * 70)
    print("FULL SCRAPE: All 478 pages of travel companies")
    print("=" * 70)
    print()
    print("This will scrape all international travel companies from:")
    print("https://quanlyluhanh.vn/index.php/cat/1001")
    print()
    print("Estimated time: 8-10 minutes")
    print("Expected companies: ~4,775")
    print()
    
    response = input("Do you want to continue? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Scraping cancelled.")
        return
    
    print("\nStarting full scrape...")
    print("-" * 70)
    
    start_time = time.time()
    
    # Create scraper with 0.7s delay (polite rate limiting)
    scraper = TravelCompanyScraper(delay=0.7)
    
    # Scrape all pages
    companies = scraper.scrape_all_pages(start_page=1, end_page=478)
    
    # Save to both CSV and JSON
    scraper.save_to_csv(companies, 'all_travel_companies.csv')
    scraper.save_to_json(companies, 'all_travel_companies.json')
    
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print()
    print("=" * 70)
    print("SCRAPING COMPLETE!")
    print("=" * 70)
    print(f"Total companies scraped: {len(companies)}")
    print(f"Time elapsed: {minutes}m {seconds}s")
    print(f"Files created:")
    print(f"  - all_travel_companies.csv")
    print(f"  - all_travel_companies.json")
    print("=" * 70)

if __name__ == '__main__':
    main()
