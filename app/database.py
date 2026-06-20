import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # reads variables from .env into the environment

DATABASE_URL = os.getenv("DATABASE_URL")

# The engine is the actual connection to Postgres
engine = create_engine(DATABASE_URL)

# Each request gets its own "session" - think of it as a conversation with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All our model classes (Transaction, Category, etc.) will inherit from this
Base = declarative_base()


def get_db():
    """
    This function provides a database session to each API request,
    and makes sure it's closed afterward even if something goes wrong.
    FastAPI will call this automatically via Depends().
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()