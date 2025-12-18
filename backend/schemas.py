from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MarketplaceRateBase(BaseModel):
    brand: str = Field(..., min_length=1, max_length=100)
    marketplace: str = Field(..., min_length=1, max_length=100)
    shipping: float = Field(..., ge=0, le=1)
    commission: float = Field(..., ge=0, le=1)


class MarketplaceRateCreate(MarketplaceRateBase):
    pass


class MarketplaceRateUpdate(BaseModel):
    shipping: Optional[float] = Field(None, ge=0, le=1)
    commission: Optional[float] = Field(None, ge=0, le=1)


class MarketplaceRateResponse(MarketplaceRateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
