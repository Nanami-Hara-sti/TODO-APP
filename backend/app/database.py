from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# データベースセッションクラス
# autocommit=False: トランザクションを自動コミットしない（手動でcommit/rollbackを行う）
# autoflush=False: クエリ実行時に自動で変更をフラッシュしない
# bind=engine: このセッションが使用するデータベースエンジンを指定
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM
Base = declarative_base()
class Orders(base):
	__tablename__ = "Orders"
	ShipName = Column(String,primary_key=True)
	Freight = Column(String)

# FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()