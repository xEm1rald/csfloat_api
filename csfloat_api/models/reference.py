from typing import Optional
from pydantic import BaseModel

class Reference(BaseModel):
    base_price: Optional[float] = None
    float_factor: Optional[float] = None
    predicted_price: Optional[float] = None
    quantity: Optional[int] = None
    last_updated: Optional[str] = None