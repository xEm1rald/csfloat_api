from typing import Optional, Any
from pydantic import BaseModel
from .statistics import Statistics

class Seller(BaseModel):
    avatar: Optional[str] = None
    away: Optional[bool] = None
    flags: Optional[int] = None
    has_valid_steam_api_key: Optional[bool] = None
    obfuscated_id: Optional[Any] = None
    online: Optional[bool] = None
    stall_public: Optional[bool] = None
    statistics: Optional[Statistics] = None
    steam_id: Optional[Any] = None
    username: Optional[str] = None
    verification_mode: Optional[str] = None