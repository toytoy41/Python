import os
# import glob
# from pathlib import Path
# import re
import shutil

class MyProg:

    def __init__(self):
        # print("Initilized!")
        pass

    def MymoveFiles(self, dum):
        fin = open("単独ファイル.txt", 'r')
        # print(dum)
        dir = 'E:/Python/MvFiles'
        os.chdir(dir)

        outdir = dir + '/images/tmp2'
        print(outdir)

        # cnt = 1
        while True:
            # if cnt > 5:
            #     break
            # cnt = cnt+1

            line = fin.readline()
            line2 = line.replace('\n', '')
            Pfile = './' + line2
            print(Pfile)
            # shutil.move(Pfile, 'outdir)
            if os.path.exists(Pfile) == True:
                print('move')
                print(Pfile)
                shutil.move(Pfile, outdir)

        fin.close()
        pass

if __name__ == '__main__':

    mF = MyProg()
    mF.MymoveFiles('test')

    exit()