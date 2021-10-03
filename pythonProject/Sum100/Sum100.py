import os

class Sum100:

    def __init__(self):
        # print("Initilized!")
        pass

    def make_pdf24_dir2dir(self, indir, outdir):
        '''
        '''

    def infile2outfile(self, infile):
        infile_name = os.path.basename(infile).split('.pdf')[0]
        outfilename = infile_name  + '_pdf24.pdf'
        return outfilename

    def get_path_fname(self, infile):
        '''
        ロングファイル名から、ディレクトリーをファイル名を返す
        :param infile: ロングファイル名
        :return: ディレクトリーをファイル名
        '''
        dir_name = os.path.dirname(infile)
        file_name = os.path.basename(infile).split('.pdf')[0]
        return dir_name, file_name

number = [1,2,3,4,5,6,7,8,9]

if __name__ == '__main__':

    pdf24pk = Sum100()
    if True:
        # pdf24pk.shougi()
        pass

    exit()

