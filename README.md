# PDF から Word への翻訳ツール

このツールは、DeepLを用いて英語のPDF文書を日本語のWord文書に変換します。論文のフォーマットによっては、うまく翻訳できないことがあります。

## 使い方

1. `pip install -r requirements.txt`を実行し、必要なモジュールをインストールする
2. `.env.example` を `.env` に改名し、DeepLのAPI_KEYを入力する。
3. 翻訳したいPDFをディレクトリに入れる。
4. `main.py` を実行する。