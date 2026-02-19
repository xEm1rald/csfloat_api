from typing import Optional, Any
from pydantic import BaseModel
from datetime import datetime

class TopBid(BaseModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    price: Optional[int] = None
    contract_id: Optional[str] = None
    state: Optional[str] = None
    active: Optional[bool] = None
    obfuscated_buyer_id: Optional[str] = None

class AuctionDetails(BaseModel):
    reserve_price: Optional[float] = None
    top_bid: Optional[TopBid] = None
    expires_at: Optional[datetime] = None
    min_next_bid: Optional[float] = None