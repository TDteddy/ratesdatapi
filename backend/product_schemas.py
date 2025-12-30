from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal


class StandardProductBase(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=500)
    brand: str = Field(..., min_length=1, max_length=100)
    cost_price: Decimal = Field(default=0, ge=0)


class StandardProductCreate(StandardProductBase):
    pass


class StandardProductUpdate(BaseModel):
    product_name: Optional[str] = Field(None, min_length=1, max_length=500)
    brand: Optional[str] = Field(None, min_length=1, max_length=100)
    cost_price: Optional[Decimal] = Field(None, ge=0)


class StandardProductResponse(StandardProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
