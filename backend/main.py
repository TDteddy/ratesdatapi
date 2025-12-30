from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import crud
import product_models
import product_schemas
import product_crud
from database import engine, get_db, sales_engine, get_sales_db

models.Base.metadata.create_all(bind=engine)
product_models.SalesBase.metadata.create_all(bind=sales_engine)

app = FastAPI(
    title="Marketplace Rates API",
    description="API for managing marketplace shipping and commission rates",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 (프론트엔드)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")


@app.get("/")
async def root():
    return {"message": "Marketplace Rates API", "docs": "/docs"}


@app.get("/api/rates", response_model=List[schemas.MarketplaceRateResponse])
async def get_all_rates(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    """모든 마켓플레이스 요율 조회"""
    rates = crud.get_all_rates(db, skip=skip, limit=limit)
    return rates


@app.get("/api/rates/brand/{brand}", response_model=List[schemas.MarketplaceRateResponse])
async def get_rates_by_brand(brand: str, db: Session = Depends(get_db)):
    """특정 브랜드의 모든 마켓플레이스 요율 조회"""
    rates = crud.get_rates_by_brand(db, brand)
    if not rates:
        raise HTTPException(status_code=404, detail=f"Brand '{brand}' not found")
    return rates


@app.get("/api/rates/{rate_id}", response_model=schemas.MarketplaceRateResponse)
async def get_rate(rate_id: int, db: Session = Depends(get_db)):
    """특정 요율 조회"""
    rate = crud.get_rate_by_id(db, rate_id)
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found")
    return rate


@app.post("/api/rates", response_model=schemas.MarketplaceRateResponse, status_code=status.HTTP_201_CREATED)
async def create_rate(rate: schemas.MarketplaceRateCreate, db: Session = Depends(get_db)):
    """새로운 마켓플레이스 요율 생성"""
    # 중복 확인
    existing_rate = crud.get_rate(db, rate.brand, rate.marketplace)
    if existing_rate:
        raise HTTPException(
            status_code=400,
            detail=f"Rate for brand '{rate.brand}' and marketplace '{rate.marketplace}' already exists"
        )

    return crud.create_rate(db, rate)


@app.put("/api/rates/{rate_id}", response_model=schemas.MarketplaceRateResponse)
async def update_rate(
    rate_id: int,
    rate_update: schemas.MarketplaceRateUpdate,
    db: Session = Depends(get_db)
):
    """마켓플레이스 요율 수정"""
    updated_rate = crud.update_rate(db, rate_id, rate_update)
    if not updated_rate:
        raise HTTPException(status_code=404, detail="Rate not found")
    return updated_rate


@app.delete("/api/rates/{rate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rate(rate_id: int, db: Session = Depends(get_db)):
    """마켓플레이스 요율 삭제"""
    success = crud.delete_rate(db, rate_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rate not found")
    return None


@app.get("/api/brands", response_model=List[str])
async def get_all_brands(db: Session = Depends(get_db)):
    """모든 브랜드 목록 조회"""
    return crud.get_all_brands(db)


@app.get("/api/marketplaces", response_model=List[str])
async def get_all_marketplaces(db: Session = Depends(get_db)):
    """모든 마켓플레이스 목록 조회"""
    return crud.get_all_marketplaces(db)


# ============== Standard Products API ==============

@app.get("/api/products", response_model=List[product_schemas.StandardProductResponse])
async def get_all_products(skip: int = 0, limit: int = 1000, db: Session = Depends(get_sales_db)):
    """모든 스탠다드 상품 조회"""
    products = product_crud.get_all_products(db, skip=skip, limit=limit)
    return products


@app.get("/api/products/search", response_model=List[product_schemas.StandardProductResponse])
async def search_products(q: str, db: Session = Depends(get_sales_db)):
    """상품명으로 검색"""
    products = product_crud.search_products(db, q)
    return products


@app.get("/api/products/brand/{brand}", response_model=List[product_schemas.StandardProductResponse])
async def get_products_by_brand(brand: str, db: Session = Depends(get_sales_db)):
    """특정 브랜드의 모든 상품 조회"""
    products = product_crud.get_products_by_brand(db, brand)
    if not products:
        raise HTTPException(status_code=404, detail=f"Brand '{brand}' not found")
    return products


@app.get("/api/products/{product_id}", response_model=product_schemas.StandardProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_sales_db)):
    """특정 상품 조회"""
    product = product_crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/api/products", response_model=product_schemas.StandardProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: product_schemas.StandardProductCreate, db: Session = Depends(get_sales_db)):
    """새로운 스탠다드 상품 생성"""
    # 중복 확인
    existing_product = product_crud.get_product_by_name(db, product.product_name)
    if existing_product:
        raise HTTPException(
            status_code=400,
            detail=f"Product '{product.product_name}' already exists"
        )

    return product_crud.create_product(db, product)


@app.put("/api/products/{product_id}", response_model=product_schemas.StandardProductResponse)
async def update_product(
    product_id: int,
    product_update: product_schemas.StandardProductUpdate,
    db: Session = Depends(get_sales_db)
):
    """스탠다드 상품 수정"""
    updated_product = product_crud.update_product(db, product_id, product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@app.delete("/api/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: Session = Depends(get_sales_db)):
    """스탠다드 상품 삭제"""
    success = product_crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None


@app.get("/api/products-brands", response_model=List[str])
async def get_product_brands(db: Session = Depends(get_sales_db)):
    """모든 상품 브랜드 목록 조회"""
    return product_crud.get_all_brands(db)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5005, reload=True)
