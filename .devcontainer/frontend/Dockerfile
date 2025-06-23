FROM node:18-alpine
WORKDIR /app

# package.jsonとlockファイルを先にコピー
COPY frontend/package*.json ./

# 依存関係をインストール
RUN npm install

# ソースコードをコピー
COPY frontend/ ./