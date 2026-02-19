from typing import List
from pydantic import BaseModel
from .listing import Listing

class Stall(BaseModel):
    listings: List[Listing] = []

    def __init__(self, **data):
        # Handle the nesting where the response usually has a 'data' key
        if "data" in data and isinstance(data["data"], list):
            super().__init__(listings=data["data"])
        else:
            super().__init__(**data)