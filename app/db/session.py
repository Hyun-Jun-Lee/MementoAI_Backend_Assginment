from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

DATABASE_URL = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PW}@maindb:{settings.DB_PORT}/{settings.DB_NAME}"


engine = create_engine(
    DATABASE_URL, pool_size=20, max_overflow=40, connect_args={"connect_timeout": 30}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    """
    호출되면 DB 연결하고 작업 완료되면 close
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
