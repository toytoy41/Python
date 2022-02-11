import os
# import pathlib
from pathlib import Path
import PyPDF2


class Rekisi:
    """
    Pdf24で見開きページをひらくと、左右に配置する。
    和書(右開き)では、右左にページを配置してほしい。
    この要求のために、Pdfファイルのページの順番をかえている。
    """

    def __init__(self):
        # print("Initilized!")
        pass

    def dir2dir(self, indir, outdir):
        os.chdir(indir)
        for f in list(Path(indir).glob('./*.pdf')):
            # f ：  は　フルパス
            self.file2dir(indir, f, outdir)

    def file2dir(self, dir_name, infile, outdir):
        # infile は　フルパス
        if dir_name is None:
            dir_name = os.path.dirname(infile)
            os.chdir(dir_name)

        # print(infile)
        infile_name = os.path.basename(infile)

        file_body_name = os.path.basename(infile).split('.pdf')[0]
        outfilename = outdir + '\\' + file_body_name  + '_pdf24.pdf'

        self.file2file(infile_name, outfilename)

    def file2file(self, infname, outfname):
        if os.path.exists(outfname):
            os.remove(outfname)

        #　infname：ここでフルパスを使ってはいけない
        pdf_reader = PyPDF2.PdfFileReader(infname)
        pdf_writer = PyPDF2.PdfFileWriter()

        pagelen = pdf_reader.getNumPages()

        dotira = True
        #   for　と　While
        if dotira == True:
            for i in range(0, pagelen, 2):
                if i == pagelen - 1:
                    if pagelen % 2 == 0:
                        pdf_writer.addPage((pdf_reader.getPage(i + 1)))
                        pdf_writer.addPage((pdf_reader.getPage(i)))
                    else:
                        pdf_writer.addPage((pdf_reader.getPage(i)))
                    break
                else:
                    pdf_writer.addPage((pdf_reader.getPage(i + 1)))
                    pdf_writer.addPage((pdf_reader.getPage(i)))
        else:
            i = 0
            while (i < pagelen):
                if i == pagelen - 1:
                    if pagelen % 2 == 0:
                        pdf_writer.addPage((pdf_reader.getPage(i + 1)))
                        pdf_writer.addPage((pdf_reader.getPage(i)))
                    else:
                        pdf_writer.addPage((pdf_reader.getPage(i)))
                    break
                else:
                    pdf_writer.addPage((pdf_reader.getPage(i + 1)))
                    pdf_writer.addPage((pdf_reader.getPage(i)))

                i = i + 2

        with open(outfname, "wb") as f:
            pdf_writer.write(f)


if __name__ == '__main__':

    basepath = 'E:\晃一\学習\社会'

    indir = basepath + '\\SCAN_00 - コピー'
    outdir = basepath + '\\SCAN_00 - コピー'

    Rekisi.dir2dir(indir, outdir)