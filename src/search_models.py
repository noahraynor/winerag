# src/search_models.py
from pydantic import BaseModel, Field
from typing import Optional

class WinerySearchRequest(BaseModel):
    query: str = Field(..., description="The type of winery or wine tour the user wants.  The entire description other than the group size and price preferences")
    max_price: Optional[int] = Field(None, description="Maximum tasting price in USD.  This is the max the group will spend at any individual winery.")
    min_group_size: Optional[int] = Field(None, description="Minimum group size supported by the winery.")
