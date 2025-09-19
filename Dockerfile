# =========================
# Stage 1: 依存関係のインストール
# =========================
FROM python:3.12-slim AS builder

WORKDIR /workspace

# pipenv をインストール
RUN pip install --no-cache-dir pipenv

# Pipfile, Pipfile.lock をコピー
COPY Pipfile Pipfile.lock ./

# 本番用の依存関係のみインストール
RUN pipenv sync --system

# =========================
# Stage 2: 本番用イメージ
# =========================
FROM python:3.12-slim AS prod

# セキュリティ: root ではなく一般ユーザーで実行
RUN useradd -m appuser
USER appuser

WORKDIR /workspace

# builder から依存関係をコピー
COPY --from=builder /usr/local /usr/local

# アプリケーションコードをコピー
COPY --chown=appuser:appuser ./src ./src

ENV PORT=8501
EXPOSE $PORT

# 本番用の起動コマンド
CMD ["sh", "-c", "streamlit run src/app.py --server.port=${PORT} --server.address=0.0.0.0 --browser.gatherUsageStats=false"]

# =========================
# Stage 3: 開発用イメージ
# =========================
FROM prod AS dev

USER root
# 開発時に便利なツールを追加
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim curl git \
 && rm -rf /var/lib/apt/lists/*

# Pipfile, Pipfile.lock をコピー（開発用依存関係インストールのため）
COPY Pipfile Pipfile.lock ./

# 開発用の依存関係をインストール
RUN pipenv sync --system --dev

USER appuser
WORKDIR /workspace

# 開発用の起動コマンド
CMD ["sh", "-c", "streamlit run src/app.py --server.port=${PORT} --server.address=0.0.0.0 --browser.gatherUsageStats=false"]
