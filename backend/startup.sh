# Azure App Service用の起動スクリプト
#!/bin/bash

# 依存関係のインストール
pip install -r requirements.txt

# データベースの初期化
python -c "
from sql_app.database import engine
from sql_app import models
models.Base.metadata.create_all(bind=engine)
print('Database initialized')
"

# Gunicornでアプリケーションを起動
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
