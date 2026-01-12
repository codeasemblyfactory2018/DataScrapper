from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ScrapedProduct(BaseModel):
    name: str
    price: float
    currency: str = "PLN"
    url: str
    shop_name: Optional[str] = None
    image_url: Optional[str] = None
    producer: Optional[str] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

class SearchResult(BaseModel):
    query: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    products: List[ScrapedProduct] = []
