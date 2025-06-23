FROM python:3.9-slim-buster
WORKDIR /app

# Pythonがモジュールを探すパスにカレントディレクトリを追加
ENV PYTHONPATH "${PYTHONPATH}:/app"

# wait-for-it.shを先にコピーして実行権限を付与
COPY .devcontainer/wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# 依存関係ファイルをコピー
COPY backend/requirements.txt ./

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY backend/ ./