from sqlalchemy.orm import Session
from typing import List, Optional, Dict
import product_models
import product_schemas
import pandas as pd
from decimal import Decimal


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


def process_excel_upload(db: Session, file_path: str) -> Dict[str, int]:
    """
    엑셀 파일을 읽어서 상품 정보를 업데이트/추가합니다.

    반환값: {"created": 생성된 수, "updated": 업데이트된 수, "errors": 오류 수}
    """
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(file_path, engine='openpyxl')

        # 필요한 컬럼 확인
        required_columns = ['대표상품', '상품명', '원가(부가세포함)']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            raise ValueError(f"필수 컬럼이 없습니다: {', '.join(missing_columns)}")

        created = 0
        updated = 0
        errors = 0

        for index, row in df.iterrows():
            try:
                # 필수 값 확인
                product_name = str(row['상품명']).strip() if pd.notna(row['상품명']) else None
                brand = str(row['대표상품']).strip() if pd.notna(row['대표상품']) else None
                cost_price = row['원가(부가세포함)']

                if not product_name or not brand:
                    errors += 1
                    continue

                # 원가 처리 (숫자가 아닌 경우 0으로 처리)
                try:
                    if pd.isna(cost_price):
                        cost_price = Decimal('0')
                    else:
                        cost_price = Decimal(str(cost_price))
                except:
                    cost_price = Decimal('0')

                # 기존 상품 확인 (상품명으로 검색)
                existing_product = get_product_by_name(db, product_name)

                if existing_product:
                    # 업데이트
                    existing_product.brand = brand
                    existing_product.cost_price = cost_price
                    updated += 1
                else:
                    # 새로 생성
                    new_product = product_models.StandardProduct(
                        product_name=product_name,
                        brand=brand,
                        cost_price=cost_price
                    )
                    db.add(new_product)
                    created += 1

            except Exception as e:
                errors += 1
                print(f"Row {index + 2} 처리 중 오류: {str(e)}")
                continue

        # 커밋
        db.commit()

        return {
            "created": created,
            "updated": updated,
            "errors": errors,
            "total": len(df)
        }

    except Exception as e:
        db.rollback()
        raise Exception(f"엑셀 파일 처리 중 오류 발생: {str(e)}")
