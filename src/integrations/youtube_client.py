from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from isodate import parse_duration  # pip install isodate

class YoutubeAPIClient:
    """
    YouTube API クライアント
    このクラスは YouTube Data API v3 を利用して、動画を検索し、
    検索結果から詳細情報を取得する機能を提供します。

    主な機能:
    1. キーワード検索による動画ID取得
    2. 動画IDリストからの詳細情報取得
    3. 上記2つを組み合わせた検索と詳細情報取得
    """

    def __init__(self, api_key: str):
        """
        YouTube API クライアントを初期化します。
        
        Args:
            api_key (str): YouTube Data API v3 の API キー
        
        Raises:
            ValueError: api_key が空の場合
        """
        if not api_key:
            raise ValueError("APIキーは空にできません。")
        
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def search_videos_ids(self, params: dict):
        """
        指定したキーワードで動画を検索し、動画IDのリストを返します。

        Args:
            q (str): 検索キーワード
            params (dict): search API に渡すパラメータ
            - maxResults (int): 取得する最大件数（デフォルト5件）
            - videoDuration (str): any, short, medium, long
            - order (str): relevance, date, viewCount, rating, title, videoCount
            - publishedAfter (str): ISO8601
            - regionCode (str): JP, US, ...
            - type: str = None
            - videoDefinition (str): any, high, standard
            - videoEmbeddable (str): true, any
            - videoCaption (str): any, closedCaption, none
            - safeSearch (str): none, moderate, strict
        
        Returns:
            list[str]: 検索結果の動画IDリスト
        
        Raises:
            ValueError: query が空の場合
            HttpError: API 呼び出しが失敗した場合
        """
        if not params.get("q"):
            raise ValueError("検索キーワードは空にできません。")

        # --- 検索用パラメータ作成 ---
        request_params = {
            "part": "snippet",
            **params
        }

        try:
            response = self.youtube.search().list(**request_params).execute()
        except HttpError as e:
            raise ValueError(f"動画検索中にエラーが発生しました: {e}") from e

        # --- 検索結果から動画IDを抽出 ---
        video_ids = [item["id"]["videoId"] for item in response.get("items", []) if item["id"].get("videoId")]
        return video_ids

    def get_video_details(self, video_ids: list):
        """
        動画IDリストから詳細情報を取得します。

        Args:
            video_ids (list[str]): 取得対象の動画IDリスト
        
        Returns:
            list[dict]: 各動画の詳細情報リスト
                        keys: title, video_id, url, description, publishedAt,
                              durationSec, viewCount, likeCount, commentCount, raw_item
        
        Raises:
            ValueError: video_ids が空の場合
            HttpError: API 呼び出しが失敗した場合
        """
        if not video_ids:
            raise ValueError("動画IDリストは空にできません。")

        try:
            response = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(video_ids)
            ).execute()
        except HttpError as e:
            raise ValueError(f"動画詳細情報取得中にエラーが発生しました: {e}") from e

        results = []
        for item in response.get("items", []):
            try:
                # ISO 8601 形式の duration を秒数に変換
                duration_sec = int(parse_duration(item["contentDetails"]["duration"]).total_seconds())
            except Exception:
                duration_sec = 0  # 変換失敗時は0秒

            stats = item.get("statistics", {})
            results.append({
                "title": item["snippet"].get("title", ""),
                "video_id": item.get("id", ""),
                "url": f"https://www.youtube.com/watch?v={item.get('id', '')}",
                "description": item["snippet"].get("description", ""),
                "publishedAt": item["snippet"].get("publishedAt", ""),
                "durationSec": duration_sec,
                "viewCount": int(stats.get("viewCount", 0)),
                "likeCount": int(stats.get("likeCount", 0)),
                "commentCount": int(stats.get("commentCount", 0)),
                "raw_item": item  # 元のAPIレスポンスを保持
            })

        return results

    def search_videos(self, params: dict):
        """
        キーワード検索と動画詳細情報取得をまとめて実行する便利関数。
        
        Args:
            params (dict): search API に渡すパラメータ
            - q: str = None
            - maxResults: int = 5
            - videoDuration: str = None
            - order: str = None
            - publishedAfter: str = None
            - type: str = None
            - regionCode: str = None
            - videoDefinition: str = None
            - videoEmbeddable: str = None
            - videoCaption: str = None
            - safeSearch: str = None
        
        Returns:
            list[dict]: 各動画の詳細情報
        
        Raises:
            ValueError, HttpError: 上記メソッドと同様
        """
        # --- 検索して動画ID取得 ---
        video_ids = self.search_videos_ids(params)
        if not video_ids:
            return []

        # --- 動画IDから詳細情報を取得 ---
        return self.get_video_details(video_ids)
