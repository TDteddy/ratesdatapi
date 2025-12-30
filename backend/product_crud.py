from sqlalchemy.orm import Session
from typing import List, Optional
import product_models
import product_schemas


def get_all_products(db: Session, skip: int = 0, limit: int = 1000) -> List[product_models.StandardProduct]:
    return db.query(product_models.StandardProduct).offset(skip).limit(limit).all()


def get_products_by_brand(db: Session, brand: str) -> List[product_models.StandardProduct]:
    return db.query(product_models.StandardProduct).filter(product_models.StandardProduct.brand == brand).all()


def get_product_by_id(db: Session, product_id: int) -> Optional[product_models.StandardProduct]:
    return db.query(product_models.StandardProduct).filter(product_models.StandardProduct.id == product_id).first()


def get_product_by_name(db: Session, product_name: str) -> Optional[product_models.StandardProduct]:
    return db.query(product_models.StandardProduct).filter(product_models.StandardProduct.product_name == product_name).first()


def create_product(db: Session, product: product_schemas.StandardProductCreate) -> product_models.StandardProduct:
    db_product = product_models.StandardProduct(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(
    db: Session,
    product_id: int,
    product_update: product_schemas.StandardProductUpdate
) -> Optional[product_models.StandardProduct]:
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None

    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return False

    db.delete(db_product)
    db.commit()
    return True


def get_all_brands(db: Session) -> List[str]:
    brands = db.query(product_models.StandardProduct.brand).distinct().all()
    return [brand[0] for brand in brands]


def search_products(db: Session, search_term: str) -> List[product_models.StandardProduct]:
    return db.query(product_models.StandardProduct).filter(
        product_models.StandardProduct.product_name.like(f"%{search_term}%")
    ).all()
