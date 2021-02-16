import os
import re
import shutil

BASE_PATH = '/RenameFiles\\'
ORIGINAL_FILE_PATH = BASE_PATH + 'Origin'
NEGATIVE_STRING = 'いっきに学び直す日本史 - コピー-'
NEGATIVE_FILE_PATH = BASE_PATH + 'NegativeFile'
NEW_PATH = BASE_PATH + 'NewFiles\\'
MY_Delfiles = []

class Rename:
    """
    ファイルの頭に'いっきに学び直す日本史 - コピー-'がついているので、削除。
    不要なファイルが’NEGATIVE_FILE_PATH’にあるので、これを除外して、
    新たなファイル名で、'NEGATIVE_FILE_PATH'にコピーする
    """

    def __init__(self):
        print("Initilized!")

    def changeFileName(self, path, ptn, delpath):
        self.getDelFile(delpath)

        os.chdir(path)
        for oldFileName in os.listdir():
            # print(oldFileName)
            if os.path.isfile(oldFileName):
                if re.match(ptn, oldFileName):
                    newFileName = oldFileName.replace(ptn, '')
                    tmp = newFileName.replace('.jpg', '')
                    # print('tmp = ' + tmp)
                    if (tmp in MY_Delfiles) == False:
                        shutil.copy(oldFileName, NEW_PATH + newFileName)
                        # os.rename(oldFileName, newFileName)
                        # print('newFileName = ' + newFileName)
                    # else:
                        # os.remove(oldFileName)

    def getDelFile(self, delpath):
        os.chdir(delpath)

        for fileName in os.listdir():
            if os.path.isfile(fileName):
                if re.search('jpg', fileName):
                    # print(fileName)
                    new = fileName.split('.')    #fileName.replace('.jpg', '')
                    MY_Delfiles.append(new[0])
                    # print(new)

        print(MY_Delfiles)

m = Rename()
m.changeFileName(ORIGINAL_FILE_PATH, NEGATIVE_STRING, NEGATIVE_FILE_PATH)
