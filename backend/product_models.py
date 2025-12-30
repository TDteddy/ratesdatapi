from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, func
from database import SalesBase


class StandardProduct(SalesBase):
    __tablename__ = "standard_products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(500), nullable=False, unique=True, comment='이지어드민 스탠다드 상품명')
    brand = Column(String(100), nullable=False, index=True, comment='브랜드 (닥터시드/딸로/테르스/에이더)')
    cost_price = Column(DECIMAL(10, 2), default=0, comment='원가 (부가세 포함)')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
