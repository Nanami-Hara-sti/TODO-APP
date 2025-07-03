#!/usr/bin/env python
"""
Azure App Service用のエントリーポイント
"""
import os
import sys

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(__file__))

from main import app

if __name__ == "__main__":
    import uvicorn
    
    # 環境変数からポート番号を取得（Azure App Serviceで自動設定される）
    port = int(os.environ.get("PORT", 8000))
    
    # データベースの初期化
    from sql_app.database import engine
    from sql_app import models
    models.Base.metadata.create_all(bind=engine)
    
    uvicorn.run(app, host="0.0.0.0", port=port)
