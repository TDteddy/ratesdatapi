from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from functools import lru_cache
from urllib.parse import quote_plus


class Settings(BaseSettings):
    # 직접 DATABASE_URL 제공 또는 개별 설정 사용
    database_url: str | None = None
    db_user: str = "root"
    db_password: str = "rootpassword"
    db_host: str = "bryze.kr"
    db_port: int = 3306
    db_name: str = "marketplace_rates"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


def get_database_url():
    settings = get_settings()

    # DATABASE_URL이 직접 제공된 경우 사용
    if settings.database_url:
        return settings.database_url

    # 개별 설정으로 URL 생성 (비밀번호 자동 인코딩)
    encoded_password = quote_plus(settings.db_password)
    return f"mysql+pymysql://{settings.db_user}:{encoded_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"


settings = get_settings()
engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
