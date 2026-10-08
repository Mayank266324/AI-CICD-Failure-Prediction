from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_DIRECTORY = PROJECT_ROOT / "data" / "database"
DATABASE_DIRECTORY.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIRECTORY / "cicd_predictions.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()