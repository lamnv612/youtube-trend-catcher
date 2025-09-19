"""YouTube動画検索ページ"""

import streamlit as st
import pandas as pd
import time
from loguru import logger
from datetime import datetime

from state import SessionManager
from integrations import OpenAIClient, YoutubeAPIClient
from config.settings import get_api_credentials, get_openai_api_key
from services import predict_search_params
from constants import (
    VIDEO_DURATION_OPTIONS,
    ORDER_OPTIONS,
    VIDEO_DEFINITION_OPTIONS,
    VIDEO_EMBEDDABLE_OPTIONS,
    VIDEO_CAPTION_OPTIONS,
)
from utils import get_key_from_label
from ui.styles import get_custom_css

# UIコンポーネント
def _render_selectbox(label, options_dict, default_value=None, help_text=None):
    """セレクトボックス描画"""
    values = list(options_dict.values())
    index = values.index(default_value) if default_value in values else 0
    selected_label = st.selectbox(label, values, index=index, help=help_text)
    return get_key_from_label(options_dict, selected_label)

def _render_number_input(label, min_val, max_val, default_val, step=1):
    """数値入力"""
    return st.number_input(label, min_value=min_val, max_value=max_val, value=default_val, step=step)

def _render_date_input(label, help_text=None):
    """日付入力（ISO形式で返す）"""
    date_val = st.date_input(label, value=None, help=help_text)
    if date_val:
        return datetime.combine(date_val, datetime.min.time()).isoformat("T") + "Z"
    return None

# フィルター描画
def _render_basic_filters():
    """基本フィルター"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        video_duration = _render_selectbox("動画の長さ", VIDEO_DURATION_OPTIONS)
    with col2:
        order = _render_selectbox("並び順", ORDER_OPTIONS)
    with col3:
        max_results = _render_number_input("取得件数", 1, 20, 5)
        st.session_state["max_results"] = max_results
    with col4:
        defaults = SessionManager.get_params()
        region_code_val = st.text_input("国コード", value=defaults.get("regionCode", "JP"))
    
    return video_duration, order, max_results, region_code_val

def _render_advanced_filters():
    """高度フィルター"""
    col1, col2, col3, col4 = st.columns(4)
    defaults = SessionManager.get_params()

    with col1:
        published_after_iso = _render_date_input(
            "公開日（以降）", 
            "指定した日付以降に公開された動画のみ表示"
        )
    with col2:
        cap_val = _render_selectbox(
            "字幕", VIDEO_CAPTION_OPTIONS, defaults.get("videoCaption")
        )
    with col3:
        video_def = _render_selectbox(
            "画質", VIDEO_DEFINITION_OPTIONS, defaults.get("videoDefinition")
        )
    with col4:
        emb_val = _render_selectbox(
            "埋め込み可能", VIDEO_EMBEDDABLE_OPTIONS, defaults.get("videoEmbeddable")
        )

    return published_after_iso, cap_val, video_def, emb_val

# AI予測処理
def _handle_ai_prediction(query, ai_client):
    """AI予測実行"""
    if not ai_client:
        return
    
    is_changed = st.session_state.get("query") != query
    if is_changed:
        with st.spinner("AI予測中..."):
            try:
                predicted_params = predict_search_params(query, ai_client)
                st.session_state["query"] = query
                SessionManager.save_params(predicted_params)
            except Exception as e:
                logger.warning(f"AI予測に失敗しました: {e}")
                st.warning("AI予測に失敗しました。手動で設定してください。")

# 検索パラメータ収集
def _collect_search_params():
    """検索パラメータ収集"""
    query = st.text_input(
        "検索キーワード（必須）",
        placeholder="検索キーワードを入力してください"
    )

    st.markdown("**フィルター**")
    video_duration, order, max_results, region_code_val = _render_basic_filters()
    published_after_iso, cap_val, video_def, emb_val = _render_advanced_filters()
    
    return {
        "q": query,
        "maxResults": max_results,
        "videoDuration": video_duration,
        "order": order,
        "publishedAfter": published_after_iso,
        "type": "video",
        "regionCode": region_code_val,
        "videoDefinition": video_def,
        "videoEmbeddable": emb_val,
        "videoCaption": cap_val,
    }

def render_search_inputs(ai_client=None):
    """検索入力UI表示"""
    params = _collect_search_params()
    _handle_ai_prediction(params["q"], ai_client)
    return params

# バリデーション
def _validate_inputs(params: dict) -> bool:
    """入力値検証"""
    errors = []
    
    if not params.get("q"):
        errors.append("検索キーワードを入力してください。")
    if params.get("maxResults", 0) < 1:
        errors.append("取得件数は1以上にしてください。")
    if len(params.get("regionCode", "")) != 2:
        errors.append("国コードは2文字にしてください。")
    
    for error in errors:
        st.error(error)
    
    return len(errors) == 0

# API検索
def _search_videos(params: dict):
    """YouTube API検索"""
    credentials = get_api_credentials()
    youtube_api_key = credentials.get("api_key")
    
    if not youtube_api_key:
        st.error("APIキーが設定されていません")
        return []

    client = YoutubeAPIClient(youtube_api_key)
    time.sleep(0.3)

    logger.info(f"検索開始: {params}")
    videos = client.search_videos(params)
    logger.info(f"検索完了: {len(videos)}件取得")
    return videos


# 動画カード生成
def _create_video_card(video):
    """動画カードHTML生成"""
    video_id = video.get("video_id", "")
    title = video.get("title", "")
    published_at = video.get("publishedAt", "")
    view_count = video.get("viewCount", 0)
    like_count = video.get("likeCount", 0)
    video_url = video.get("url", "")
    
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    short_title = title[:50] + "..." if len(title) > 50 else title
    
    return f"""
    <div class="video-card">
        <div class="video-title">{short_title}</div>
        <div class="video-iframe">
            <iframe width="100%" height="200" src="{embed_url}" frameborder="0" allowfullscreen></iframe>
        </div>
        <div class="video-metrics">
            <div class="video-metric"><div class="video-metric-label">閲覧数</div><div class="video-metric-value">{view_count:,}</div></div>
            <div class="video-metric"><div class="video-metric-label">いいね数</div><div class="video-metric-value">{like_count:,}</div></div>
            <div class="video-metric"><div class="video-metric-label">公開日</div><div class="video-metric-value">{published_at[:10] if published_at else "不明"}</div></div>
        </div>
        <div class="video-card-footer">
            <a href="{video_url}" target="_blank" class="video-link">🔗 YouTubeで見る</a>
        </div>
    </div>
    """

def _render_video_list(videos: list):
    """動画リスト表示"""
    if not videos:
        st.warning("結果が見つかりませんでした")
        return

    st.markdown(get_custom_css(), unsafe_allow_html=True)
    videos_per_row = 3
    
    for i in range(0, len(videos), videos_per_row):
        row_videos = videos[i:i + videos_per_row]
        cols = st.columns(videos_per_row)
        
        for j, video in enumerate(row_videos):
            if j < len(cols):
                with cols[j]:
                    st.markdown(_create_video_card(video), unsafe_allow_html=True)
        
        if i + videos_per_row < len(videos):
            st.markdown("<br>", unsafe_allow_html=True)

# テーブル表示
def _create_dataframe(videos: list):
    """DataFrame作成"""
    return pd.DataFrame([{
        "タイトル": v.get("title", ""),
        "URL": v.get("url", ""),
        "説明": v.get("description", ""),
        "公開日時": v.get("publishedAt", ""),
        "長さ(秒)": v.get("durationSec", 0),
        "閲覧数": v.get("viewCount", 0),
        "いいね数": v.get("likeCount", 0),
        "コメント数": v.get("commentCount", 0)
    } for v in videos])

def _render_table_view(videos: list):
    """テーブル表示・CSVダウンロード"""
    if not videos:
        st.warning("結果が見つかりませんでした")
        return

    df = _create_dataframe(videos)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="📥 CSVでダウンロード",
        data=csv,
        file_name="youtube_videos.csv",
        mime="text/csv",
    )

# 結果表示
def _render_results(videos: list):
    """結果タブ表示"""
    if not videos:
        st.warning("結果が見つかりませんでした")
        return

    tab1, tab2 = st.tabs(["🎬 動画リスト", "📊 テーブル表示"])
    
    with tab1:
        _render_video_list(videos)
    with tab2:
        _render_table_view(videos)


# AIクライアント初期化
def _init_ai_client():
    """AIクライアント初期化"""
    try:
        openai_api_key = get_openai_api_key()
        return OpenAIClient(api_key=openai_api_key)
    except Exception as e:
        logger.warning(f"AI client初期化に失敗しました: {e}")
        return None

# メインページ
def show_search_video_page():
    """YouTube動画検索ページ"""
    st.header("📋 YouTube動画検索")

    ai_client = _init_ai_client()
    params = render_search_inputs(ai_client)

    if st.button("🔍 検索"):
        if not _validate_inputs(params):
            return

        with st.spinner("検索中..."):
            try:
                videos = _search_videos(params)
                _render_results(videos)
            except Exception as e:
                logger.error("検索中にエラー発生: {}", e, exc_info=True)
                st.error(f"検索中にエラーが発生しました: {str(e)}")
