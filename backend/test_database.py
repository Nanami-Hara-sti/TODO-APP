"""
テスト用のデータベース設定
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql_app.database import Base
from sql_app.models import Todo

# テスト用のインメモリSQLiteデータベース
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_test_database():
    """テスト用データベースを作成"""
    Base.metadata.create_all(bind=engine)

def get_test_db():
    """テスト用データベースセッションを取得"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def cleanup_test_database():
    """テスト用データベースをクリーンアップ"""
    Base.metadata.drop_all(bind=engine)
