FROM node:18-alpine
WORKDIR /workspace/frontend

# package.jsonとlockファイルを先にコピー
COPY frontend/package*.json ./

# 依存関係をインストール
RUN npm install

# ソースコードをコピー
COPY frontend/ ./

# ポート3000を公開
EXPOSE 3000

# Reactアプリを起動
CMD ["npm", "start"]