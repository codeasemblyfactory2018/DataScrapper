import httpx
from bs4 import BeautifulSoup
from typing import List
from src.scrapers.base import BaseScraper
from src.models.product import ScrapedProduct
from loguru import logger

class StaticScraper(BaseScraper):
    async def search(self, query: str) -> List[ScrapedProduct]:
        url = self.search_url_template.format(query=query.replace(" ", "+"))
        logger.info(f"Searching {self.domain} for: {query} -> {url}")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        headers.update(self.headers)

        async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=15.0) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
            except Exception as e:
                logger.error(f"Failed to fetch {url}: {str(e)}")
                return []

            return self._parse(response.text)

    def _parse(self, html: str) -> List[ScrapedProduct]:
        soup = BeautifulSoup(html, "html.parser")
        products = []
        
        container_selector = self.selectors.get("product_container")
        items = soup.select(container_selector)
        
        for item in items:
            try:
                name_elem = item.select_one(self.selectors.get("name"))
                price_elem = item.select_one(self.selectors.get("price"))
                link_elem = item.select_one(self.selectors.get("link"))
                
                if not name_elem or not price_elem:
                    continue
                    
                name = name_elem.get_text(strip=True)
                price_text = price_elem.get_text(strip=True)
                price = self._clean_price(price_text)
                
                # Handle relative URLs
                link = link_elem["href"] if link_elem else ""
                if link and link.startswith("/"):
                    link = self.base_url + link
                
                products.append(ScrapedProduct(
                    name=name,
                    price=price,
                    url=link,
                    shop_name=self.domain
                ))
            except Exception as e:
                logger.warning(f"Error parsing item on {self.domain}: {e}")
                
        return products
