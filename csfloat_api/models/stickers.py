from typing import Optional
from pydantic import BaseModel, Field

class StickerReference(BaseModel):
    price: Optional[float] = None
    quantity: Optional[int] = None
    updated_at: Optional[str] = None

class Sticker(BaseModel):
    sticker_id: Optional[int] = Field(None, alias="stickerId")
    slot: Optional[int] = None
    wear: Optional[float] = None
    offset_x: Optional[float] = None
    offset_y: Optional[float] = None
    icon_url: Optional[str] = None
    name: Optional[str] = None
    reference: Optional[StickerReference] = None