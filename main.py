import fitz  # PyMuPDF
import deepl
from docx import Document
import re
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# organics-02-00008-v3
# Keto Enol Tautomerism Ethyl Acetoacetate 1962
pdf_dir = "pdf"

# 1番目のファイルを取得
pdfs = os.listdir(pdf_dir)
pdf = pdfs[0]

input_pdf = os.path.join(pdf_dir, pdf)

# PDFファイルを開く
doc = fitz.open(input_pdf)

# Wordドキュメントを新規作成
output_doc = Document()

try:
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

                # Acknowledgmentを含む場合
                if "Acknowledgment" in text:
                    break
                
                if text:
                    result = translator.translate_text(text, source_lang="EN", target_lang="JA")
                else:
                    print("翻訳するテキストが空です")

                print(result.text)

                # 結果を追加
                texts.append(result.text)

        # Wordドキュメントに翻訳結果を追加
        for trans_text in texts:
            output_doc.add_paragraph(trans_text)

    # 保存とクリーンアップ
    output_doc.save(f'translated_docx/{pdf}.docx')
    doc.close()

except Exception as e:
    print(f"エラーが発生しました: {e}")
    output_doc.save(f'translated_docx/{pdf}_error.docx')
    doc.close()


# pdfを移動
os.rename(input_pdf, f'translated_pdf/{pdf}')