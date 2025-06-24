FROM node:18-alpine
WORKDIR /workspace/frontend

# package.jsonとlockファイルを先にコピー
COPY frontend/package*.json ./

# 依存関係をインストール
RUN npm install

# ソースコードをコピー
COPY frontend/ ./