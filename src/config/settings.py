"""
設定管理モジュール
環境変数の安全な読み込み
"""

import os
from dotenv import load_dotenv


def get_api_credentials():
    """API認証情報を安全に取得"""
    load_dotenv()
    return {
        "api_key": os.getenv("YOUTUBE_API_KEY"),
    }


def get_openai_api_key():
    """OpenAI API認証情報を安全に取得"""
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

