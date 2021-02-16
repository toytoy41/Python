import os
import re

MY_PATH = 'E:\ETC\PDF'
MY_PTN ='いっきに学び直す日本史 - コピー-'

class Rename:
    """
    ファイル名の頭に'いっきに学び直す日本史 - コピー-'がついているので、
    この部分削除した新たなファイルを作る。
    """

    def __init__(self):
        print("Initilized!")

    def ren(self, path, ptn):
        os.chdir(path)

        for name in os.listdir():
            # print(name)
            if os.path.isfile(name):
                if re.match(ptn, name):
                    new = name.replace(ptn,'')
                    os.rename(name, new)
                    print(new)

    # def getDelFile(self, delfiles):
    #     os.chdir(delfiles)
    #
    #     for name in os.listdir():
    #         # print(name)
    #         if os.path.isfile(name):
    #             if re.match('.jpg', name):
    #                 new = name.replace('.jpg', '')
    #                 MY_Delfiles.append(new)
    #                 print(new)

m = Rename(MY_PATH,MY_PTN)
m.ren()
