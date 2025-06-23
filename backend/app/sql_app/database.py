from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'
# DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)
# engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()