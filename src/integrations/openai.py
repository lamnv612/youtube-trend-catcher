from openai import OpenAI
from constants import OPENAI_MODEL

class OpenAIClient:
    """
    OpenAI呼び出しクライアント
    """

    def __init__(self, api_key: str):
        """
        Args:
            api_key (str): OpenAI APIキー
        """
        self.client = OpenAI(api_key=api_key)

    def ask(self, prompt: str, system_prompt: str | None = None, model: OPENAI_MODEL = OPENAI_MODEL.GPT_4O_MINI) -> str:
        """
        指定したプロンプトに対してモデルから応答を取得

        Args:
            prompt (str): ユーザーの入力
            system_prompt (str, optional): システムプロンプト
            model (OPENAI_MODEL, optional): 使用モデル（デフォルト GPT_4O_MINI）

        Returns:
            str: モデルからの応答
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content

