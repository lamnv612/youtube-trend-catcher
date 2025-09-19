"""YouTube検索APIのパラメータ予測処理モジュール"""

import json
from integrations import OpenAIClient

# --- AI用のプロンプトテンプレート ---
PROMPT_TEMPLATE = """
あなたはYouTube検索APIのパラメータ予測アシスタントです。
ユーザーが入力した検索キーワードから、以下のパラメータを推測してください。
※ 参考資料：https://developers.google.com/youtube/v3/docs/search/list?hl=ja

必須パラメータ（文字列として出力してください）:
- type: "動画" / "チャンネル" / "プレイリスト"
- safeSearch: "制限なし" / "適度に制限" / "厳しく制限"
- regionCode: 例: "JP", "US", etc.
- videoDefinition: "すべて" / "高画質" / "標準画質"
- videoEmbeddable: "すべて" / "埋め込み可能のみ"
- videoCaption: "すべて" / "字幕あり" / "字幕なし"

注意事項:
1. 出力はJSON形式のみでお願いします。
2. 値は必ず上記の候補のいずれかにしてください。
3. 不要な説明や文章は一切加えないでください。
4. Booleanではなく、必ずダブルクォート付きの文字列として出力してください。

検索キーワード: "{query}"
"""

# --- 検索パラメータ予測関数 ---
def predict_search_params(query: str, ai_client: OpenAIClient) -> dict:
    """
    指定した検索キーワードから、YouTube APIのパラメータをAIで予測して返す関数

    Args:
        query (str): ユーザーの検索キーワード
        ai_client (OpenAIClient): OpenAI呼び出し用クライアント

    Returns:
        dict: 予測されたパラメータ（type, safeSearch, regionCode, videoDefinition, videoEmbeddable, videoCaption）
    """

    # プロンプトにキーワードを埋め込む
    prompt = PROMPT_TEMPLATE.format(query=query)

    # AIに問い合わせ
    response_text = ai_client.ask(prompt)

    # JSONパース
    try:
        # 不要な ```json ``` や ``` を削除
        cleaned_response_text = response_text.replace("```json", "").replace("```", "")
        predicted_params = json.loads(cleaned_response_text)
    except json.JSONDecodeError:
        # パース失敗時はデフォルト値
        predicted_params = {
            "type": "動画",
            "safeSearch": "制限なし",
            "regionCode": "JP",
            "videoDefinition": "すべて",
            "videoEmbeddable": "すべて",
            "videoCaption": "すべて"
        }

    return predicted_params
