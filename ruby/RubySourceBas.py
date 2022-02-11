import sys
import re
import shutil

# filename= 'Watashitachino_Kashiwa_0.html'
# taiouhyou = {'章': 'しょう', '発足': 'ほっそく', '際': 'さい', '募集': 'ぼしゅう',
#              '制定': 'せいてい', '機': 'き', '名称': 'めいしょう', '若潮': 'わかしお',
#              '記念緑化': 'きねんりょっか', '一致': 'いっち', '選': 'えら', '市政': 'しせい', '周年': 'しゅうねん',
#              '広': 'ひろ', '守': 'まも', '住': 'す', '太陽': 'たいよう', '姿': 'すがた', '発展': 'はってん',
#              '象徴': 'しょうちょう',
#              '資料': 'しりょう', '様子': 'ようす', '公共': 'こうきょう', '農家': 'のうか', '農': 'のう', '事': 'じ',
#              '利用': 'りよう', '災害': 'さいがい', '地震': 'じしん', '伝統': 'でんとう', '先人': 'せんじん',
#              '郷土': 'きょうど', '残': 'のこ'}  # '農':'のう',

fileDic = {1:'K0.txt', 2:'K10.txt', 3:'K11.txt', 4:'K12.txt', 5:'K121.txt',
           6:'K122.txt', 7:'K123.txt', 8:'K21.txt', 9:'K211.txt', 10:'K212.txt',
           11:'K22.txt', 12:'K23.txt', 13:'K30.txt', 14:'K31.txt', 15:'K32.txt',
           16:'K41.txt', 17:'K42.txt', 18:'K43.txt', 19:'K44.txt', 20:'K51.txt',
           21:'K52.txt', 22:'K61.txt', 23:'K62.txt', 24:'K71.txt', 25:'K72.txt',
           26:'KOrikomi.txt', 27:'KFront.txt'}

indir = './in/'
outdir = './out/'
originLines = ''
fileNumbers = [1,2]
rubyDict ={}

class PutRuby():
    inFile = ''
    outFile = ''
    tmpFile = 'tmp.html'

    def __init__(self):
        '''
        sfdasf
        '''
        # self.site=site
        # self.num = 1
        pass

    def getFile(self, fileNumber):
        '''
        1ファイルのルビ辞書Dictを作成する
        :param fileNumber:
        :return:''
        '''
        # fileNumber=1
        with open(fileDic[fileNumber], 'rt', encoding='utf-8') as file:
            newline_break = ""
            for readline in file:
                line_strip = readline.strip()
                newline_break += line_strip

        (k, v) = newline_break.split(';')

        line_strip0 = v.replace('{', '').replace('}', '')
        line_strip1 = line_strip0.replace(' ', '', 200)

        # print(k)
        # print(line_strip1)

        line_strip2 = line_strip1.split(',')

        newDict = {}
        for term in line_strip2:
            # print(term)
            term2 = term.replace(" ", '', 100)
            # print(term2)
            (k2, v2) = term2.split(':')
            newDict[k2] = v2

        print(newDict)
        return k, newDict

    def SourceBase(self, fileNumber):
        fileNumber = 2
        filename, KanjiDict = self.getFile(fileNumber)

        print('filename : ' + filename)

        self.inFile = indir + filename
        self.outFile = outdir + filename

        with open(self.inFile, 'rt', encoding='utf-8') as f:
            originLines = f.readlines()

        fout = open(self.tmpFile, 'wt', encoding='utf-8')

        startFlg = False

        for inLine in originLines:
            new = inLine
            if startFlg == False:
                # print(new)
                if re.search('<body>', new):
                    startFlg = True
            else:
                con2=0
                for kanji in KanjiDict.keys():
                    if re.search(kanji, new):
                        if re.search('<rb>' + kanji + '.*</rb>', new):
                            print("no" + new, end="")
                        else:
                            kana = KanjiDict.get(kanji)
                            new = re.sub(kanji,
                                         '<ruby> <rb>' + kanji + '</rb> <rp>（</rp> <rt>' + kana + '</rt> <rp>）</rp> </ruby>',
                                         new)
                            # print("yes" + new, end="")
                            # print(new)

            fout.write(new)

        fout.close()
        shutil.copyfile(self.tmpFile, self.outFile)

    def KeyBase(self):

        for filename in rubyDict.keys():
            with open(indir + filename,encoding='utf-8') as f:
                lineList = f.readlines()

            outlines = ''

            taiouhyou = rubyDict.get(filename)

            for kanji in taiouhyou.keys():
                outlines = ''
                for line in lineList:
                    changeflag = False

                    if re.search(kanji, line):
                        # print(line, end="")
                        # print("a")
                        if re.search('<rb>' + kanji + '.*</rb>', line):
                            print("no" + line, end="")
                        else:
                            kana = taiouhyou.get(kanji)
                            new = re.sub(kanji,'<ruby> <rb>' + kanji + '</rb> <rp>（</rp> <rt>' + kana + '</rt> <rp>）</rp> </ruby>',
                                   line)
                            print("yes" + line, end="")
                            print(new)

                            changeflag = True
                            outlines = outlines + new

                    if changeflag == False:
                        outlines = outlines + line

                linelist = outlines

            print(outlines)

            outfile = outdir + filename
            with open(outfile, 'wt', encoding='utf-8') as outfile:
                outfile.writelines(outlines)

def go():
    ruby = PutRuby()
    ruby.SourceBase(2)

if __name__ == '__main__':

    go()

    sys.exit()
