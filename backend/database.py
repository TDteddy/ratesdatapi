from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from functools import lru_cache
from urllib.parse import quote_plus


class Settings(BaseSettings):
    # 직접 DATABASE_URL 제공 또는 개별 설정 사용
    database_url: str | None = None
    sales_database_url: str | None = None
    db_user: str = "root"
    db_password: str = "rootpassword"
    db_host: str = "bryze.kr"
    db_port: int = 3306
    db_name: str = "marketplace_rates"
    sales_db_name: str = "seller_mapping"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


def get_database_url(db_name: str | None = None):
    settings = get_settings()

    # DATABASE_URL이 직접 제공된 경우 사용
    if db_name == "sales" and settings.sales_database_url:
        return settings.sales_database_url
    elif db_name is None and settings.database_url:
        return settings.database_url

    # 개별 설정으로 URL 생성 (비밀번호 자동 인코딩)
    encoded_password = quote_plus(settings.db_password)
    database_name = settings.sales_db_name if db_name == "sales" else settings.db_name
    return f"mysql+pymysql://{settings.db_user}:{encoded_password}@{settings.db_host}:{settings.db_port}/{database_name}"


settings = get_settings()

# marketplace_rates 데이터베이스 (기존)
engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# sales 데이터베이스 (신규)
sales_engine = create_engine(get_database_url("sales"))
SalesSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sales_engine)
SalesBase = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_sales_db():
    db = SalesSessionLocal()
    try:
        yield db
    finally:
        db.close()
