import fitz  # PyMuPDF
import deepl
from docx import Document
import re
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

input_pdf = 'schneider-et-al-2015-development-of-a-novel-fingerprint-for-chemical-reactions-and-its-application-to-large-scale.pdf'

# PDFファイルを開く
doc = fitz.open(input_pdf)

# Wordドキュメントを新規作成
output_doc = Document()

# DeepLのAPIキーとトランスレーターの初期化
API_KEY = os.getenv('DEEPL_API_KEY')
translator = deepl.Translator(API_KEY)

# 各ページを順に処理
for i, page in enumerate(doc):
    blocks = page.get_text("blocks")  # ページ上のテキストブロックを取得
    texts = []

    for block in blocks:
        text = block[4]  # テキスト内容
        if text.strip():  # 空白のブロックは無視
            # テキストのクリーニング
            text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)

            # 翻訳を実行
            result = translator.translate_text(text, source_lang="EN", target_lang="JA")
            print(result.text)

            # 結果を追加
            texts.append(result.text)

    # Wordドキュメントに翻訳結果を追加
    for trans_text in texts:
        output_doc.add_paragraph(trans_text)

# 保存とクリーンアップ
output_doc.save(f'{input_pdf}_translated_output.docx')
doc.close()
