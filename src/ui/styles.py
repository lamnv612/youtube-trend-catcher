"""
スタイル定義モジュール
StreamlitアプリケーションのカスタムCSS
"""


def get_custom_css():
    """カスタムCSSを返す"""
    return """
    <style>
        /* 全体的な余白設定 */
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: none;
            margin: 0;
        }

        /* サイドバーのスタイリング */
        .css-1d391kg {
            width: 280px !important;
        }

        /* サイドバー内のボタンスタイリング */
        .stSidebar .stButton > button {
            width: 100%;
            margin-bottom: 0.5rem;
            border-radius: 0.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .stSidebar .stButton > button[data-testid="baseButton-primary"] {
            background-color: #ff4b4b;
            border-color: #ff4b4b;
            color: white;
        }

        .stSidebar .stButton > button[data-testid="baseButton-secondary"] {
            background-color: transparent;
            border-color: #484856;
            color: #ffffff;
        }

        .stSidebar .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        /* ハッシュタグカード */
        .hashtag-card {
            background-color: #2a2a35;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid transparent;
            margin-bottom: 0.5rem;
            transition: all 0.3s ease;
        }
        .hashtag-card:hover {
            border-color: #ff4b4b;
        }

        /* ナビゲーションの視覚的改善 */
        .stSidebar .stMarkdown h1 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            margin-top: 0;
            padding-top: 0;
            text-align: center;
        }

        /* サイドバーの余白調整 */
        .stSidebar > div:first-child {
            padding-top: 1rem;
        }

        /* サイドバー内のコンテンツ余白を調整 */
        .st-emotion-cache-16txtl3 {
            padding-top: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        .stSidebar .stMarkdown h3 {
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            color: #ff4b4b;
        }

        /* selectboxとbuttonの高さを揃える */
        div[data-testid="stSelectbox"] > div > div > div,
        .stSelectbox > div > div > div > div {
            height: auto !important;
            min-height: auto !important;
        }

        .stButton > button {
            height: 2.75rem !important;
            padding-top: 0.375rem !important;
            padding-bottom: 0.375rem !important;
        }

        /* 動画カードのスタイリング */
        .video-card {
            background-color: #2a2a35;
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid #484856;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            height: 100%;
            display: flex;
            flex-direction: column;
            min-height: 400px;
        }
        
        .video-card:hover {
            border-color: #ff4b4b;
            box-shadow: 0 4px 16px rgba(255,75,75,0.2);
            transform: translateY(-2px);
        }
        
        .video-card-content {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        .video-card-footer {
            margin-top: auto;
            padding-top: 0.5rem;
        }
        
        .video-title {
            font-size: 1rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 0.75rem;
            line-height: 1.3;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-height: 2.6rem;
        }
        
        .video-iframe {
            border-radius: 0.5rem;
            overflow: hidden;
            margin-bottom: 0.75rem;
        }
        
        .video-metrics {
            display: flex;
            gap: 0.25rem;
            margin-bottom: 0.75rem;
        }
        
        .video-metric {
            background-color: #2a2a2f;
            padding: 0.375rem;
            border-radius: 0.25rem;
            text-align: center;
            flex: 1;
            border: 1px solid #484856;
        }
        
        .video-metric-label {
            font-size: 0.7rem;
            color: #9ca3af;
            margin-bottom: 0.125rem;
        }
        
        .video-metric-value {
            font-size: 0.8rem;
            font-weight: 600;
            color: #ffffff;
        }
        
        .video-description {
            font-size: 0.875rem;
            color: #d1d5db;
            line-height: 1.5;
            margin-bottom: 0.75rem;
        }
        
        .video-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: #ff4b4b;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }
        
        .video-link:hover {
            color: #ff6b6b;
        }
        
        /* 動画グリッドレイアウト */
        .video-grid-container {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .video-grid-item {
            flex: 1;
            min-width: 250px;
            max-width: calc(33.333% - 0.5rem);
        }
        
        /* フィルター部分のスタイリング */
        .filter-container {
            background-color: #2a2a35;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid #484856;
        }
        
        .filter-title {
            color: #ff4b4b;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .filter-grid,
        .filter-grid-2 {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.5rem;
        }
        
        .filter-grid {
            margin-bottom: 0.5rem;
        }
        
        .filter-item {
            background-color: #2a2a2f;
            border-radius: 0.375rem;
            padding: 0.5rem;
            border: 1px solid #484856;
            transition: all 0.3s ease;
        }
        
        .filter-item:hover {
            border-color: #ff4b4b;
            background-color: #2f2f35;
        }
        
        /* レスポンシブ対応 */
        @media (max-width: 1200px) {
            .video-grid-item {
                min-width: 300px;
                max-width: calc(50% - 0.5rem);
            }
            .filter-grid, .filter-grid-2 {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
            .css-1d391kg {
                width: 250px !important;
            }
            .video-grid-item {
                min-width: 100%;
                max-width: 100%;
            }
            .filter-grid, .filter-grid-2 {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """