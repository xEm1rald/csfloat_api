from typing import Optional, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime

from .statistics import Statistics
from .me import User
from .item import Item

class SteamOffer(BaseModel):
    id: Optional[int] = None
    state: Optional[int] = None
    is_from_seller: bool = False
    can_cancel_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    deadline_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Contract(BaseModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    type: Optional[str] = None
    price: float = 0
    state: Optional[str] = None
    seller: Optional[User] = None
    item: Optional[Item] = None
    is_seller: bool = False
    is_watchlisted: bool = False
    watchers: int = 0
    sold_at: Optional[datetime] = None

class Trade(BaseModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    buyer_id: Optional[str] = None
    buyer: Optional[User] = None
    seller_id: Optional[str] = None
    seller: Optional[User] = None
    contract_id: Optional[int] = None
    accepted_at: Optional[datetime] = None
    state: Optional[Literal["pending", "verified", "failed", "cancelled"]] = None
    verification_mode: Optional[str] = None
    steam_offer: Optional[SteamOffer] = None
    verify_sale_at: Optional[datetime] = None
    inventory_check_status: Optional[Any] = None
    trade_protection_ends_at: Optional[datetime] = None
    contract: Optional[Contract] = None
    trade_url: Optional[str] = None
    trade_token: Optional[str] = None
    wait_for_cancel_ping: bool = False
    is_settlement_period: bool = False