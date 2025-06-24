FROM python:3.9-slim-buster
WORKDIR /workspace/backend

ENV PYTHONPATH "${PYTHONPATH}:/workspace/backend"

COPY .devcontainer/backend/wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# 依存関係ファイルをコピー
COPY backend/requirements.txt ./

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
