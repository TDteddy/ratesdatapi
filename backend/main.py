from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

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
