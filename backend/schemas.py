# backend/schemas.py
from pydantic import BaseModel, HttpUrl, ConfigDict
from datetime import datetime
from typing import List, Optional

# Request schemas
class TrackProductRequest(BaseModel):
    url: HttpUrl

# Response schemas
class PriceHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    price: float
    currency: str
    recorded_at: datetime

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    url: str
    name: str
    retailer: str
    currency: str
    current_price: float
    lowest_price: Optional[float]
    highest_price: Optional[float]
    created_at: datetime
    updated_at: datetime
    last_checked_at: datetime

class ProductWithHistoryResponse(ProductResponse):
    # Config is inherited automatically, no need to redefine
    price_history: List[PriceHistoryResponse]

# Legacy response for backward compatibility
class ProductTrackResponse(BaseModel):
    name: str
    price: float
    currency: str
    url: str
    retailer: str
    tracked: bool = True
    product_id: Optional[int] = None