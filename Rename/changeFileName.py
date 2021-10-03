import os
import glob
from pathlib import Path
import re

class FRename:

    def __init__(self):
        # print("Initilized!")
        pass

    def changeFname(self, dir, stringDel, renFlag):
        os.chdir(dir)
        print(stringDel)
        for f in list(Path(dir).glob('*.jpg')):
            # f ：  は　フルパス
            fileName = os.path.basename(f)
            if re.search(stringDel, fileName) != None :
                print(fileName)
                newName = fileName.replace(stringDel,'')
                # newName = fileName.replace(stringDel,'PX1')
                print(newName)
                if renFlag == 1:
                    os.rename(fileName, newName)

        pass

if __name__ == '__main__':

    cF = FRename()
    # dir = 'E:\\tmp\\P87-97_４市のうつりかわり.img'
    # dir = 'E:\\Python\\Rename\\P87-97_４市のうつりかわり.img'
    # cF.changeFname(indir, "_４市のうつりかわり-")
    # dir = 'E:\Python\Rename\P74-81_①火事からくらしを守る.img'
    # dir = 'E:\Python\Rename\P82_86②事故や事件からくらしを守る.img'
    # dir = 'E:\Python\Rename\P87-97_４市のうつりかわり.img'
    # dir = 'E:\Python\Rename\P98-105_５住みよいくらしをつくる.img'
    # dir = 'E:\Python\Rename\P106-117_②ごみのしょ理と利用.img'
    # dir = 'E:\Python\Rename\P118-121_６きょう土の伝統・文化と先人たち.img'
    # dir = 'E:\Python\Rename\P122-125_柏市災害時安心MAP.img'
    # dir = 'E:\Python\Rename\P126-138_７郷土をひらく.img'
    # dir = 'E:\Python\Rename\P139-147_のこしたいもの　伝えたいもの.img'
    # dir = 'E:\Python\Rename\【折込-1】写真でみる中核市・柏.img'
    dir = 'E:\哲郎\柏市\Work\＜PDF＞【令和3年度】わたしたちの柏\\tmp\images'
    # cF.changeFname(dir, "_１わたしたちのまち　みんなのまち")
    # delstring = '_①学校のまわり'
    delstring = '_②工場の仕事'
    cF.changeFname(dir, delstring, 1)


    exit()
