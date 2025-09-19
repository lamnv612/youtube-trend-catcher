"""
Streamlit セッション状態管理モジュール
検索パラメータの状態を一元管理（key を保存）
"""

import streamlit as st

class SessionManager:
    """検索パラメータセッション管理クラス"""

    # デフォルト値 (key を保存)
    DEFAULT_STATES = {
        "query": "",
        "type": "動画",
        "safeSearch": "制限なし",
        "regionCode": "JP",
        "videoDefinition": "すべて",
        "videoEmbeddable": "すべて",
        "videoCaption": "すべて",
    }

    @staticmethod
    def initialize_session_state():
        for key, value in SessionManager.DEFAULT_STATES.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def reset_all():
        for key, value in SessionManager.DEFAULT_STATES.items():
            st.session_state[key] = value

    @staticmethod
    def save_params(params: dict):
        for key, value in params.items():
            st.session_state[key] = value

    @staticmethod
    def get_params() -> dict:
        return {key: st.session_state.get(key) for key in SessionManager.DEFAULT_STATES.keys()}


