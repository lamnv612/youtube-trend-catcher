# Trend Catcher

トレンドを分析してマーケティングバナー用の構成要素を抽出するStreamlitアプリ。

## 概要

YouTube Data APIからトレンド動画/タグを取得し、AI分析により動画構成パターンを抽出してバナー作成用の要素を提供します。

## セットアップ

```bash
# 依存関係のインストール
pipenv install --dev

# 仮想環境の有効化
pipenv shell

# アプリ起動
streamlit run src/app.py --server.runOnSave true
```

### 技術スタック
- **フロントエンド**: Streamlit
- **API統合**: YouTube Data API、OpenAI GPT
- **データ処理**: Python (pandas、plotly)
- **状態管理**: セッション状態による5段階ワークフロー制御

## 開発環境

### VS Code Dev Container

- このプロジェクトは Dev Container に対応しています。Docker 上で依存関係が自動セットアップされ、ローカル環境を汚さずに開発できます。
- 手順:
  1. VS Code でリポジトリを開く
  2. コマンドパレットで "Dev Containers: Reopen in Container" を実行
  3. 初回は Docker イメージのビルドに時間がかかります
  4. コンテナ起動後、自動的に依存関係がインストールされます

### アプリの起動（コンテナ内）
```bash
streamlit run src/app.py --server.runOnSave true
```

- ブラウザで [http://localhost:8501](http://localhost:8501) にアクセスできます。
