from sqlalchemy import Column, Integer, String, Float, UniqueConstraint, DateTime, func
from database import Base


class MarketplaceRate(Base):
    __tablename__ = "marketplace_rates"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(100), nullable=False, index=True)
    marketplace = Column(String(100), nullable=False, index=True)
    shipping = Column(Float, nullable=False)
    commission = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('brand', 'marketplace', name='unique_brand_marketplace'),
    )
