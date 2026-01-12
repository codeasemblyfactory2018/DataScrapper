from abc import ABC, abstractmethod
from typing import List, Dict, Any
import yaml
import os
from src.models.product import ScrapedProduct

class BaseScraper(ABC):
    def __init__(self, domain: str, config_path: str = "config/selectors.yaml"):
        self.domain = domain
        self.config = self._load_config(config_path, domain)
        self.selectors = self.config.get("selectors", {})
        self.headers = self.config.get("headers", {})
        self.base_url = self.config.get("base_url", "")
        self.search_url_template = self.config.get("search_url", "")

    def _load_config(self, path: str, domain: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            return {}
        with open(path, "r") as f:
            full_config = yaml.safe_load(f)
            return full_config.get("strategies", {}).get(domain, {})

    @abstractmethod
    async def search(self, query: str) -> List[ScrapedProduct]:
        pass

    def _clean_price(self, price_str: str) -> float:
        # Polish prices often use comma as decimal separator: "99,99 zł"
        if not price_str:
            return 0.0
        
        # Remove non-numeric chars except comma/dot
        clean = "".join(c for c in price_str if c.isdigit() or c in ",.")
        clean = clean.replace(",", ".")
        
        try:
            return float(clean)
        except ValueError:
            return 0.0
