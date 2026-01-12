import asyncio
import sys
import os
from loguru import logger

# Add src to path so we can run from backend root
sys.path.append(os.path.join(os.getcwd(), "src"))

from src.scrapers.factory import ScraperFactory

async def main():
    # Example search
    query = "Dolina Noteci mokra karma dla kota"
    domains = ["ceneo.pl"] # Allegro requires playwright install and is slower for quick test
    
    for domain in domains:
        try:
            scraper = ScraperFactory.get_scraper(domain)
            results = await scraper.search(query)
            
            logger.info(f"Found {len(results)} results on {domain}")
            for product in results[:5]: # Show first 5
                print(f"- {product.name}: {product.price} {product.currency}")
                
        except Exception as e:
            logger.error(f"Error scraping {domain}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
