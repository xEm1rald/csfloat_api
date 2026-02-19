from typing import Optional
from pydantic import BaseModel

class BuyOrders(BaseModel):
    id: Optional[str] = None
    created_at: Optional[str] = None
    expression: Optional[str] = None
    qty: Optional[int] = None
    price: Optional[int] = None