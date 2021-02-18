import os
import pathlib
from pathlib import Path
import PyPDF2

class Pdf24:

    def __init__(self):
        # print("Initilized!")
        pass

    def dir2dir(self, indir, outdir):
        '''
        indirにあるすべてのPDFファイルを変換する。
        :param indir: PDFのもとファイルがあるディレクトリー
        :param outdir: 出力用ディレクトリー
        :return:
        '''
        os.chdir(indir)
        for f in list(Path(indir).glob('./*.pdf')):
            # outfile = outdir + '\\' + self.infile2outfile(f)
            self.file2dir(f, outdir)

    # def infile2outfile(self, infile):
    #     infile_name = os.path.basename(infile).split('.pdf')[0]
    #     outfilename = infile_name  + '_pdf24.pdf'
    #     return outfilename

    def get_path_fname(self, infile):
        '''
        ロングファイル名から、ディレクトリーをファイル名を返す
        :param infile: ロングファイル名
        :return: ディレクトリーをファイル名
        '''
        dir_name = os.path.dirname(infile)
        file_name = os.path.basename(infile).split('.pdf')[0]
        return dir_name, file_name

    def file2dir(self, infname, outdir):
        '''
        infname=PDFファイルをoutdirに書き込む
        :param infname:
        :param outdir:
        :return:
        '''
        items = self.get_path_fname(infname)
        filename= items[1] + '.pdf'
        outfilename = outdir + '\\' + items[1].split('.')[0]  + '_pdf24.pdf'

        self.file2file(filename, outfilename)

    def file2file(self, infname, outfname):
        if os.path.exists(outfname):
            os.remove(outfname)

        pdf_reader = PyPDF2.PdfFileReader(infname)
        pdf_writer = PyPDF2.PdfFileWriter()

        lastNum = pdf_reader.getNumPages()

        for i in range(0, lastNum, 2):
            if i >= lastNum - 1:
                if lastNum % 2 == 0:
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

        pass

    def pdf24file(self, indir, outdir, infname, outfname):

        # os.chdir(inPath)
        outfname = outdir + '\\' + outfname
        if os.path.exists(outfname):
            os.remove(outfname)
        infname = indir + '\\' + infname

        pdf_reader = PyPDF2.PdfFileReader(infname)
        pdf_writer = PyPDF2.PdfFileWriter()

        lastNum = pdf_reader.getNumPages()

        dotira = False
        #   for　と　While
        if dotira == True:
            for i in range(0, lastNum, 2):
                if i >= lastNum - 1:
                    if lastNum % 2 == 0:
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
            while (i < lastNum):
                if i == lastNum - 1:
                    if lastNum % 2 == 0:
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

    # def shougi(self, indir, outdir):
    #     # pdfdir = basepath + '\Pdf\歴史'
    #     os.chdir(indir)
    #     for f in list(Path(indir).glob('./*.pdf')):
    #         self.file2dir(f, outdir)

if __name__ == '__main__':

    # print("IN")
    hp = True
    if hp:
        basepath = 'E:\Amazon'
    else:
        basepath = 'E:\BOOK'

    indir = basepath + '\\Pdf\歴史'
    outdir = basepath + '\\Pdf24\歴史'

    Pdf24().dir2dir(indir, outdir)

    exit()
