from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
import models
import schemas


def get_all_rates(db: Session, skip: int = 0, limit: int = 1000) -> List[models.MarketplaceRate]:
    return db.query(models.MarketplaceRate).offset(skip).limit(limit).all()


def get_rates_by_brand(db: Session, brand: str) -> List[models.MarketplaceRate]:
    return db.query(models.MarketplaceRate).filter(models.MarketplaceRate.brand == brand).all()


def get_rate(db: Session, brand: str, marketplace: str) -> Optional[models.MarketplaceRate]:
    return db.query(models.MarketplaceRate).filter(
        and_(
            models.MarketplaceRate.brand == brand,
            models.MarketplaceRate.marketplace == marketplace
        )
    ).first()


def get_rate_by_id(db: Session, rate_id: int) -> Optional[models.MarketplaceRate]:
    return db.query(models.MarketplaceRate).filter(models.MarketplaceRate.id == rate_id).first()


def create_rate(db: Session, rate: schemas.MarketplaceRateCreate) -> models.MarketplaceRate:
    db_rate = models.MarketplaceRate(**rate.model_dump())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate


def update_rate(
    db: Session,
    rate_id: int,
    rate_update: schemas.MarketplaceRateUpdate
) -> Optional[models.MarketplaceRate]:
    db_rate = get_rate_by_id(db, rate_id)
    if not db_rate:
        return None

    update_data = rate_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_rate, key, value)

    db.commit()
    db.refresh(db_rate)
    return db_rate


def delete_rate(db: Session, rate_id: int) -> bool:
    db_rate = get_rate_by_id(db, rate_id)
    if not db_rate:
        return False

    db.delete(db_rate)
    db.commit()
    return True


def get_all_brands(db: Session) -> List[str]:
    brands = db.query(models.MarketplaceRate.brand).distinct().all()
    return [brand[0] for brand in brands]


def get_all_marketplaces(db: Session) -> List[str]:
    marketplaces = db.query(models.MarketplaceRate.marketplace).distinct().all()
    return [marketplace[0] for marketplace in marketplaces]
