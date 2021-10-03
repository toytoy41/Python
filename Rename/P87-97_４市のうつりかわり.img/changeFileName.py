import os
import glob
from pathlib import Path

class FRename:

    def __init__(self):
        # print("Initilized!")
        pass

    def changeFname(self, dir, stringDel):
        # os.chdir(dir)
        print(stringDel)
        for f in list(Path(dir).glob('*.jpg')):
            # f ：  は　フルパス
            fileName = os.path.basename(f)
            print(fileName)
            newName = fileName.replace(stringDel,'')
            os.rename(fileName, newName)
            # print(fileName.replace('４市のうつりかわり-',''))
            # print(file_body_name)
        pass

if __name__ == '__main__':

    indir = 'E:\\tmp\P87-97_４市のうつりかわり.img'
    cF = FRename()
    cF.changeFname(indir, "４市のうつりかわり-")

    exit()
