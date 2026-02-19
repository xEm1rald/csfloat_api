from typing import Optional, Dict, List, Any, Set
from pydantic import BaseModel
from .statistics import Statistics
from datetime import datetime

class Preferences(BaseModel):
    offers_enabled: Optional[bool] = None
    max_offer_discount: Optional[int] = None

class FirebaseMessaging(BaseModel):
    platform: Optional[int] = None
    last_updated: Optional[datetime] = None

class User(BaseModel):
    steam_id: Optional[str] = None
    username: Optional[str] = None
    flags: Optional[int] = None
    avatar: Optional[str] = None
    background_url: Optional[str] = None
    email: Optional[str] = None
    balance: Optional[int] = None
    pending_balance: Optional[int] = None
    stall_public: Optional[bool] = None
    away: Optional[bool] = None
    trade_token: Optional[str] = None
    payment_accounts: Optional[Dict[str, Any]] = None
    api_key: str = ""
    statistics: Optional[Statistics] = None
    preferences: Optional[Preferences] = None
    know_your_customer: Optional[str] = None
    extension_setup_at: Optional[datetime] = None
    firebase_messaging: Optional[FirebaseMessaging] = None
    stripe_connect: Optional[Set[Any]] = None
    has_valid_steam_api_key: Optional[bool] = None
    obfuscated_id: Optional[str] = None
    online: Optional[bool] = None
    fee: Optional[float] = None
    withdraw_fee: Optional[float] = None
    subscriptions: Optional[List[Any]] = None
    has_2fa: Optional[bool] = None

class Me(BaseModel):
    user: Optional[User] = None
    pending_offers: Optional[int] = None
    actionable_trades: Optional[int] = None