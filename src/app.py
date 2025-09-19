"""
Youtube トレンドキャッチャー - メインアプリケーション
"""

import streamlit as st

from ui.styles import get_custom_css
from state.session_manager import SessionManager
from ui.views import show_search_video_page


def setup_app():
    """アプリケーションの初期設定"""
    # ページ設定
    st.set_page_config(
        page_title="YouTube トレンドキャッチャー",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # カスタムCSS適用
    st.markdown(get_custom_css(), unsafe_allow_html=True)


def route_pages():
    """ページルーティング"""
    page_map = {
        "動画検索": show_search_video_page
    }

    current_page = "動画検索"
    if current_page in page_map:
        page_map[current_page]()
    else:
        st.error(f"不明なページ: {current_page}")


def main():
    setup_app()
    SessionManager.initialize_session_state()
    route_pages()


if __name__ == "__main__":
    main()
