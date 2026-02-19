from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from .seller import Seller
from .reference import Reference
from .item import Item
from .auction import AuctionDetails

class Listing(BaseModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    type: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    state: Optional[str] = None
    seller: Optional[Seller] = None
    reference: Optional[Reference] = None
    item: Optional[Item] = None
    is_seller: Optional[bool] = None
    min_offer_price: Optional[float] = None
    max_offer_discount: Optional[float] = None
    is_watchlisted: Optional[bool] = None
    watchers: Optional[int] = None
    auction_details: Optional[AuctionDetails] = None
    sold_at: Optional[datetime] = None