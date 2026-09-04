from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Session
from collections.abc import Generator

from app.core.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

class Base(DeclarativeBase):
    pass