import markdown
import pdfkit
import wkhtmltopdf

text = '''
 # 今日やること
 - 切手を買う
 - xxの資料を作る
 '''
# HTMLに変換
md = markdown.Markdown() # ---(*1)
body = md.convert(text) # ---(*2)
# HTML出力用のヘッダを足す # ---(*3)
html = '<html lang="ja"><meta charset="utf-8"><body>'
html += '<style> body { font-size: 8em; } </style>'
html += body + '</body></html>'
# PDF出力
pdfkit.from_string(html, "test.pdf") # --- (*4)