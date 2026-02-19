from typing import Optional
from pydantic import BaseModel

class Statistics(BaseModel):
    median_trade_time: Optional[float] = None
    total_avoided_trades: Optional[int] = None
    total_failed_trades: Optional[int] = None
    total_trades: Optional[int] = None
    total_verified_trades: Optional[int] = None
    total_sales: Optional[int] = None      # Added for 'Me' compatibility
    total_purchases: Optional[int] = None  # Added for 'Me' compatibility