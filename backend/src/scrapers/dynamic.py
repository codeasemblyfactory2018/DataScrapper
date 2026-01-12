from playwright.async_api import async_playwright
from typing import List
from src.scrapers.base import BaseScraper
from src.models.product import ScrapedProduct
from loguru import logger

class DynamicScraper(BaseScraper):
    async def search(self, query: str) -> List[ScrapedProduct]:
        url = self.search_url_template.format(query=query.replace(" ", "+"))
        logger.info(f"Dynamic searching {self.domain} for: {query}")
        
        products = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Wait for product containers
                container_selector = self.selectors.get("product_container")
                await page.wait_for_selector(container_selector, timeout=10000)
                
                # Extraction logic
                items = await page.query_selector_all(container_selector)
                for item in items:
                    try:
                        name_elem = await item.query_selector(self.selectors.get("name"))
                        price_elem = await item.query_selector(self.selectors.get("price"))
                        link_elem = await item.query_selector(self.selectors.get("link"))
                        
                        if not name_elem or not price_elem:
                            continue
                            
                        name = await name_elem.inner_text()
                        price_text = await price_elem.inner_text()
                        # Some dynamic sites have prices in aria-label or specific formats
                        if not any(c.isdigit() for c in price_text):
                            price_text = await price_elem.get_attribute("aria-label") or ""

                        price = self._clean_price(price_text)
                        link = await link_elem.get_attribute("href") if link_elem else ""
                        
                        if link and link.startswith("/"):
                            link = self.base_url + link
                            
                        products.append(ScrapedProduct(
                            name=name.strip(),
                            price=price,
                            url=link,
                            shop_name=self.domain
                        ))
                    except Exception as e:
                        logger.debug(f"Parsing error on dynamic item: {e}")
            except Exception as e:
                logger.error(f"Playwright error on {self.domain}: {e}")
            finally:
                await browser.close()
                
        return products
