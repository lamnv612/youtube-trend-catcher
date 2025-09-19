def get_key_from_label(options: dict, label: str) -> str:
    """
    ラベルからキーを取得
    Args:
        options (dict): オプションの辞書
        label (str): ラベル
    Returns:
        str: キー
    """
    for k, v in options.items():
        if v == label:
            return k
    raise KeyError(f"ラベル {label} が見つかりません")
    