import os
import pathlib
from pathlib import Path

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from glob import glob

def convert_pdf_to_txt(path): # 引数にはPDFファイルパスを指定
    print(path)
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    laparams.detect_vertical = True # Trueにすることで綺麗にテキストを抽出できる
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    print('OK')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 0
    caching = True
    pagenos=set()
    fstr = ''
    num = 0
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,caching=caching, check_extractable=True):
        interpreter.process_page(page)

        str = retstr.getvalue()
        print(str)
        fstr += str

    fp.close()
    device.close()
    retstr.close()
    return fstr

file_list = glob('E:\\Python\\Work\\tmp\\*.pdf')
print(list(glob('E:\\Python\\Work\\tmp\\*.pdf')))
# pdfdir = 'E:\\Python\\Work\\tmp'
# os.chdir(pdfdir)
# print(list(Path(pdfdir).glob('./*.pdf')))

result_list = []
for item in file_list:
    # print(item)
    result_txt = convert_pdf_to_txt(item)
    # print(result_txt)
    result_list.append(result_txt)

allText = ','.join(result_list) # PDFごとのテキストが配列に格納されているので連結する

file = open('pdf.txt', 'wt')  #書き込みモードでオープン
file.write(allText)

pass