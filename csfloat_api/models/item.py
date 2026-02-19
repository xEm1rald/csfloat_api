from typing import Optional, List, Any
from pydantic import BaseModel
from datetime import datetime
from .stickers import Sticker

class Item(BaseModel):
    asset_id: Optional[int] = None
    def_index: Optional[int] = None
    paint_index: Optional[float] = None
    paint_seed: Optional[float] = None
    float_value: Optional[float] = None
    icon_url: Optional[str] = None
    d_param: Optional[int] = None
    is_stattrak: Optional[bool] = None
    is_souvenir: Optional[bool] = None
    rarity: Optional[int] = None
    quality: Optional[int] = None
    market_hash_name: Optional[str] = None
    low_rank: Optional[int] = None
    stickers: Optional[List[Sticker]] = None
    tradable: Optional[Any] = None # Original used both bool and int
    inspect_link: Optional[str] = None
    has_screenshot: Optional[bool] = None
    cs2_screenshot_id: Optional[int] = None
    cs2_screenshot_at: Optional[datetime] = None
    is_commodity: Optional[bool] = None
    type: Optional[str] = None
    rarity_name: Optional[str] = None
    type_name: Optional[str] = None
    item_name: Optional[str] = None
    wear_name: Optional[str] = None
    description: Optional[str] = None
    collection: Optional[str] = None
    badges: Optional[List[Any]] = None
    serialized_inspect: Optional[str] = None
    gs_sig: Optional[str] = None