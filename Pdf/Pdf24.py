import os
# import pathlib
from pathlib import Path
import PyPDF2


class Pdf24:

    def __init__(self):
        # print("Initilized!")
        pass

    def dir2dir(self, indir, outdir):
        # os.chdir(indir)
        for f in list(Path(indir).glob('./*.pdf')):
            self.file2dir(f, outdir)

    def file2dir(self, infname, outdir):
        items = self.get_path_fname(infname)
        indir = items[0]

        os.chdir(indir)
        filename= items[1] + '.pdf'
        outfilename = outdir + '\\' + items[1].split('.')[0]  + '_pdf24.pdf'

        self.file2file(filename, outfilename)

    def get_path_fname(self, infile):
        dir_name = os.path.dirname(infile)
        file_name = os.path.basename(infile).split('.pdf')[0]
        return dir_name, file_name

    def file2file(self, infname, outfname):
        if os.path.exists(outfname):
            os.remove(outfname)

        pdf_reader = PyPDF2.PdfFileReader(infname)
        pdf_writer = PyPDF2.PdfFileWriter()

        lastnum = pdf_reader.getNumPages()

        for i in range(0, lastnum, 2):
            if i >= lastnum - 1:
                if lastnum % 2 == 0:
                    pdf_writer.addPage((pdf_reader.getPage(i + 1)))
                    pdf_writer.addPage((pdf_reader.getPage(i)))
                else:
                    pdf_writer.addPage((pdf_reader.getPage(i)))
                break
            else:
                pdf_writer.addPage((pdf_reader.getPage(i + 1)))
                pdf_writer.addPage((pdf_reader.getPage(i)))

        with open(outfname, "wb") as f:
            pdf_writer.write(f)


if __name__ == '__main__':

    hp = True
    if hp:
        basepath = 'E:\Amazon'
    else:
        basepath = 'E:\BOOK'

    pdf24pk = Pdf24()
    one_file = False
    if one_file:
        pdf24pk.file2dir(basepath + '\Pdf\将棋\もはや死角なし！　進化版 極限早繰り銀.pdf', basepath + '\PDF24\将棋')
        pdf24pk.file2dir(basepath + '\Pdf\将棋\エルモ囲い急戦.pdf', basepath + '\PDF24\将棋')
    else:
        pdf24pk.dir2dir(basepath + '\Pdf\将棋', basepath + '\PDF24\将棋')

