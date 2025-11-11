#!/usr/bin/env python3
"""
Command-line interface for the Travel Company Scraper
"""

import argparse
import sys
from scraper import TravelCompanyScraper


def main():
    parser = argparse.ArgumentParser(
        description='Scrape travel company data from quanlyluhanh.vn'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='travel_companies.csv',
        help='Output filename (default: travel_companies.csv)'
    )
    
    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['csv', 'json'],
        default='csv',
        help='Output format (default: csv)'
    )
    
    parser.add_argument(
        '-s', '--start-page',
        type=int,
        default=1,
        help='Starting page number (default: 1)'
    )
    
    parser.add_argument(
        '-e', '--end-page',
        type=int,
        default=None,
        help='Ending page number (default: scrape all pages)'
    )
    
    parser.add_argument(
        '-d', '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Auto-detect format from filename if not specified
    if args.output.endswith('.json') and args.format == 'csv':
        args.format = 'json'
    elif args.output.endswith('.csv') and args.format == 'json':
        args.format = 'csv'
    
    print(f"Travel Company Scraper")
    print(f"=" * 50)
    print(f"Starting page: {args.start_page}")
    print(f"Ending page: {args.end_page if args.end_page else 'All pages'}")
    print(f"Output format: {args.format}")
    print(f"Output file: {args.output}")
    print(f"Delay: {args.delay}s")
    print(f"=" * 50)
    print()
    
    # Create scraper instance
    scraper = TravelCompanyScraper(delay=args.delay)
    
    # Scrape data
    try:
        print("Scraping data...")
        companies = scraper.scrape_all_pages(
            start_page=args.start_page,
            end_page=args.end_page
        )
        
        if not companies:
            print("No companies found!")
            sys.exit(1)
        
        print(f"\nSuccessfully scraped {len(companies)} companies")
        
        # Save data
        print(f"Saving to {args.output}...")
        if args.format == 'json':
            scraper.save_to_json(companies, args.output)
        else:
            scraper.save_to_csv(companies, args.output)
        
        print(f"\n✓ Done! Data saved to {args.output}")
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
