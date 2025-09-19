---
applyTo: '**'
---

- コード内で環境変数の追加・削除が行われた場合、`.env.sample`へも反映が行われていることを確認してください
- `.env.sample`に定義された環境変数が、`.github/aws/task-definitions-*.json`の`containerDefinitions.environment`もしくは`containerDefinitions.secrets`にも定義されていることを確認してください
- `Dockerfile`のイメージタグは省略されておらず、かつ`latest`タグが使用されていないことを確認してください
- `Pipfile`や`requirements.txt`に記載されているパッケージのメジャーバージョンが固定されていることを確認してください
- `Pipfile`と`Pipfile.lock`の内容が一致していることを確認してください
- `.vscode/settings.json`の設定に基づいて、コードのフォーマットが適切に行われていることを確認してください