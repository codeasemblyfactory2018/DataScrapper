from typing import Dict, Type
import yaml
import os
from src.scrapers.base import BaseScraper
from src.scrapers.static import StaticScraper
from src.scrapers.dynamic import DynamicScraper

class ScraperFactory:
    @staticmethod
    def get_scraper(domain: str, config_path: str = "config/selectors.yaml") -> BaseScraper:
        # Load config to check type
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found at {config_path}")
            
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            strategy_config = config.get("strategies", {}).get(domain)
            
            if not strategy_config:
                # Fallback to default or raise error
                strategy_type = "static"
            else:
                strategy_type = strategy_config.get("type", "static")
        
        if strategy_type == "dynamic":
            return DynamicScraper(domain, config_path)
        else:
            return StaticScraper(domain, config_path)
