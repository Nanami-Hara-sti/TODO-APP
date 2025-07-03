# Azure TODOアプリ デプロイメント手順

## 前提条件
- Azure アカウント
- Azure CLI のインストール
- Git リポジトリ（GitHub推奨）

## 1. Azure リソースの作成

### バックエンド用 App Service の作成
```bash
# リソースグループの作成
az group create --name todo-app-rg --location "Japan East"

# App Service プランの作成
az appservice plan create \
  --name todo-backend-plan \
  --resource-group todo-app-rg \
  --sku B1 \
  --is-linux

# Web App の作成
az webapp create \
  --resource-group todo-app-rg \
  --plan todo-backend-plan \
  --name your-todo-backend-app \
  --runtime "PYTHON|3.10" \
  --startup-file "startup.py"
```

### フロントエンド用 Static Web Apps の作成
```bash
# Static Web Apps の作成
az staticwebapp create \
  --name your-todo-frontend-app \
  --resource-group todo-app-rg \
  --location "East Asia" \
  --source https://github.com/yourusername/TODO-APP \
  --branch main \
  --app-location "/frontend" \
  --output-location "build"
```

## 2. 環境変数の設定

### バックエンド
```bash
# CORS設定用の環境変数
az webapp config appsettings set \
  --resource-group todo-app-rg \
  --name your-todo-backend-app \
  --settings \
    WEBSITES_ENABLE_APP_SERVICE_STORAGE=true \
    PYTHONPATH=/home/site/wwwroot
```

### フロントエンド
`.env.production` ファイルで設定：
```
REACT_APP_API_BASE_URL=https://your-todo-backend-app.azurewebsites.net
```

## 3. デプロイ方法

### 方法1: Azure CLI を使用
```bash
# バックエンドのデプロイ
cd backend
az webapp up \
  --resource-group todo-app-rg \
  --name your-todo-backend-app \
  --runtime "PYTHON:3.10"

# フロントエンドのデプロイ
cd ../frontend
npm run build
az staticwebapp upload \
  --name your-todo-frontend-app \
  --resource-group todo-app-rg \
  --source-location ./build
```

### 方法2: GitHub Actions を使用
1. GitHub リポジトリの Settings > Secrets で以下を設定：
   - `AZURE_BACKEND_PUBLISH_PROFILE`: App Service の公開プロファイル
   - `AZURE_STATIC_WEB_APPS_API_TOKEN`: Static Web Apps のデプロイトークン

2. コードをmainブランチにプッシュすると自動デプロイされます

### 方法3: Docker Container を使用
```bash
# Docker イメージのビルドとプッシュ
cd backend
docker build -f Dockerfile.azure -t your-todo-backend .
docker tag your-todo-backend youracr.azurecr.io/todo-backend:latest
docker push youracr.azurecr.io/todo-backend:latest

# Container Instance の作成
az container create \
  --resource-group todo-app-rg \
  --name todo-backend-container \
  --image youracr.azurecr.io/todo-backend:latest \
  --ports 8000 \
  --dns-name-label your-todo-backend
```

## 4. CORS設定の確認

バックエンドで以下のオリジンが許可されていることを確認：
```python
origins = [
    "https://your-todo-frontend-app.azurestaticapps.net",
    "http://localhost:3000",  # 開発用
]
```

## 5. データベース設定

### SQLite（デフォルト）
- 開発・テスト環境に適している
- ファイルベースのデータベース

### Azure SQL Database（本番推奨）
```bash
# Azure SQL Database の作成
az sql server create \
  --name your-sql-server \
  --resource-group todo-app-rg \
  --location "Japan East" \
  --admin-user sqladmin \
  --admin-password YourPassword123!

az sql db create \
  --resource-group todo-app-rg \
  --server your-sql-server \
  --name todo-database \
  --service-objective Basic
```

## 6. 監視とログ

### Application Insights の設定
```bash
az monitor app-insights component create \
  --app todo-app-insights \
  --location "Japan East" \
  --resource-group todo-app-rg
```

## 7. カスタムドメインとSSL（オプション）

### カスタムドメインの設定
```bash
# App Service にカスタムドメインを追加
az webapp config hostname add \
  --webapp-name your-todo-backend-app \
  --resource-group todo-app-rg \
  --hostname api.yourdomain.com

# Static Web Apps にカスタムドメインを追加
az staticwebapp hostname set \
  --name your-todo-frontend-app \
  --resource-group todo-app-rg \
  --hostname yourdomain.com
```

## トラブルシューティング

### 一般的な問題
1. **CORS エラー**: バックエンドのCORS設定を確認
2. **API接続エラー**: フロントエンドの API_BASE_URL を確認
3. **デプロイエラー**: Azure ポータルでログを確認

### ログの確認
```bash
# App Service のログストリーム
az webapp log tail \
  --resource-group todo-app-rg \
  --name your-todo-backend-app
```

## セキュリティ設定

### 認証の追加（オプション）
```bash
# Azure AD 認証の設定
az webapp auth update \
  --resource-group todo-app-rg \
  --name your-todo-backend-app \
  --enabled true \
  --action LoginWithAzureActiveDirectory
```
