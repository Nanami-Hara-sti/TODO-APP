from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

Base = declarative_base()
class Orders(Base):
	__tablename__ = "Orders"
	ShipName = Column(String,primary_key=True)
	Freight = Column(String)

# DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)     

# FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()