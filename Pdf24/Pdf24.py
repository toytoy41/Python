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
        for f in Path(indir).glob('./*.pdf'):
            # outfile = outdir + '\\' + self.infile2outfile(f)
            print(f)
            self.file2dir(f, outdir)

    def file2dir(self, infname, outdir):
        # os.chdir('E:\\Amazon\\Pdf\\将棋')
        items = self.get_path_fname(infname)
        # indir = items[0]
        # filename= items[1] + '.pdf'

        # outfilename = outdir + '\\' + self.infile2outfile(infname)
        outfilename = outdir + '\\' + items[1].split('.')[0]  + '_pdf24.pdf'
        print(outfilename)
        self.file2file(infname, outfilename)

    # def infile2outfile(self, infile):
    #     infile_name = os.path.basename(infile).split('.pdf')[0]
    #     outfilename = infile_name + '_pdf24.pdf'
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

    def file2file(self, infname, outfname):
        print("infname : " + infname.name)
        print("outfname : " + outfname)

        if os.path.exists(outfname):
            print("outfname : " + outfname)
            os.remove(outfname)

        if os.path.exists(infname):
            print("InFile OK:")

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

        pass


if __name__ == '__main__':

    pdf24pk = Pdf24()
    one_file = False
    if one_file:
        pdf24pk.file2dir('E:\BOOK\Pdf\将棋\もはや死角なし 進化版 極限早繰り銀.pdf', 'E:\BOOK\Pdf24\Work')
        pdf24pk.file2dir('E:\BOOK\Pdf\将棋\エルモ囲い急戦.pdf', 'E:\BOOK\Pdf24\Work')
    else:
        # pdf24pk.dir2dir('E:\\Amazon\\Pdf\\将棋', 'E:\\Amazon\\PDF24\\work')
        pdfdir = 'E:\BOOK\Pdf\将棋'
        for f in Path(pdfdir).glob('./*.pdf'):
            print(f)
            pdf24pk.file2dir(f, 'E:\BOOK\Pdf24\Work')


    #     pdfFile = 'E:\Amazon\Pdf\将棋\急所を直撃！とっておきの雁木破り.pdf'
    #     pdfdir = 'E:\Amazon\Pdf\将棋'
    #     os.chdir(pdfdir)
    #     print(list(Path(pdfdir).glob('./*.pdf')))

    # pdfFile = 'E:\Amazon\Pdf\将棋\急所を直撃！とっておきの雁木破り.pdf'
    # pdfdir = 'E:\Amazon\Pdf\将棋'
    # os.chdir(pdfdir)
    # print(list(Path(pdfdir).glob('./*.pdf')))
    #
    # pdf24pk = Pdf24()
    # for f in list(Path(pdfdir).glob('./*.pdf')):
    #     pcode: str = pdf24pk.make_pdf24(f, 'E:\Amazon\PDF24')

    exit()

    # pcode:str = pdf24PK.make_pdf24(pdfFile, 'E:\Amazon\PDF24')


    # def make_pdf24(self, pdfPath, inFname, outFile):
    #
    #     os.chdir(pdfPath)
    #     if os.path.exists(outFile):
    #         os.remove(outFile)
    #
    #     pdf_reader = PyPDF2.PdfFileReader(inFname)
    #     pdf_writer = PyPDF2.PdfFileWriter()
    #
    #     lastNum = pdf_reader.getNumPages()
    #
    #     for i in range(0, lastNum, 2):
    #         if i >= lastNum - 1:
    #             if lastNum % 2 == 0:
    #                 pdf_writer.addPage((pdf_reader.getPage(i + 1)))
    #                 pdf_writer.addPage((pdf_reader.getPage(i)))
    #             else:
    #                 pdf_writer.addPage((pdf_reader.getPage(i)))
    #             break
    #         else:
    #             pdf_writer.addPage((pdf_reader.getPage(i + 1)))
    #             pdf_writer.addPage((pdf_reader.getPage(i)))
    #
    #     with open(outFile, "wb") as f:
    #         pdf_writer.write(f)

    # def make_pdf240(self, in_fname, out_dir):
    #     self.make_pdf24(os.path.dirname(in_fname), in_fname, self.get_outfile(in_fname))

    # def make_pdf24_file2dir(self, infile, outdir):
    #     '''
    #     indirにあるすべてのPDFファイルを変換する。
    #     :param indir: PDFのもとファイルがあるディレクトリー
    #     :param outdir: 出力用ディレクトリー
    #     :return:
    #     '''
    #     outfile = outdir + '\\' + self.infile2outfile(infile)
    #     self.make_pdf24_file2file(infile, outfile)

    # def get_path_fname(self, infile):
    #     '''
    #     ロングファイル名から、ディレクトリーをファイル名を返す
    #     :param infile: ロングファイル名
    #     :return: ディレクトリーをファイル名
    #     '''
    #     dir_name = os.path.dirname(infile)
    #     file_name = os.path.basename(infile).split('.pdf')[0]
    #     return dir_name, file_name

    # def make_pdf24file(self, indir, outdir, infname, outfname):
    #
    #     # os.chdir(inPath)
    #     outfname = outdir + '\\' + outfname
    #     if os.path.exists(outfname):
    #         os.remove(outfname)
    #     infname = indir + '\\' + infname
    #
    #     pdf_reader = PyPDF2.PdfFileReader(infname)
    #     pdf_writer = PyPDF2.PdfFileWriter()
    #
    #     lastNum = pdf_reader.getNumPages()
    #
    #     for i in range(0, lastNum, 2):
    #         if i >= lastNum - 1:
    #             if lastNum % 2 == 0:
    #                 pdf_writer.addPage((pdf_reader.getPage(i + 1)))
    #                 pdf_writer.addPage((pdf_reader.getPage(i)))
    #             else:
    #                 pdf_writer.addPage((pdf_reader.getPage(i)))
    #             break
    #         else:
    #             pdf_writer.addPage((pdf_reader.getPage(i + 1)))
    #             pdf_writer.addPage((pdf_reader.getPage(i)))
    #
    #     with open(outfname, "wb") as f:
    #         pdf_writer.write(f)

    # def shougi(self):
    #     pdfFile = 'E:\Amazon\Pdf\将棋\急所を直撃！とっておきの雁木破り.pdf'
    #     pdfdir = 'E:\Amazon\Pdf\将棋'
    #     os.chdir(pdfdir)
    #     print(list(Path(pdfdir).glob('./*.pdf')))
    #
    #     # pdf24pk = Pdf24()
    #     for f in list(Path(pdfdir).glob('./*.pdf')):
    #         self.make_pdf24_file2dir(f, 'E:\Amazon\PDF24')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
