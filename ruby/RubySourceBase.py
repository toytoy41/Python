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

# fileDic = {1:'K0.txt', 2:'K10.txt', 3:'K11.txt', 4:'K12.txt', 5:'K121.txt',
#            6:'K122.txt', 7:'K123.txt', 8:'K21.txt', 9:'K211.txt', 10:'K212.txt',
#            11:'K22.txt', 12:'K23.txt', 13:'K30.txt', 14:'K31.txt', 15:'K32.txt',
#            16:'K41.txt', 17:'K42.txt', 18:'K43.txt', 19:'K44.txt', 20:'K51.txt',
#            21:'K52.txt', 22:'K61.txt', 23:'K62.txt', 24:'K71.txt', 25:'K72.txt',
#            26:'KOrikomi.txt', 27:'KFront.txt'}
fileDic = {1:'K0.txt', 2:'K10.txt', 3:'K11.txt', 4:'K12.txt', 5:'K121.txt',
           6:'K122.txt', 7:'K123.txt', 8:'K21.txt', 9:'K211.txt', 10:'K212.txt',
           11:'K22.txt', 12:'K23.txt', 14:'K31.txt', 15:'K32.txt',
           16:'K41.txt', 20:'K51.txt',
           21:'K52.txt', 22:'K61.txt', 23:'K62.txt', 24:'K71.txt', 25:'K72.txt',
           26:'KOrikomi.txt', 27:'KFront.txt', 30:'nav.txt'}

#　42，43，44　は　41に含まれる
#　30はルビなし
# るび　発展形
# ファイルの中のキー毎に
# '道'
# ①　 変更するもの出現回をリストにする。
# [1,2,5]
# ②　 変更の対象外
escapeDic = {3:{'道':[[1,2,5],['道じゅん','この道','ある道','鉄橋','道を','道は','道だ']],
	'橋':[[1],['鉄橋']]}
}

CHANGENUM = 2

indir = './in/'
outdir = './out/'
originLines = ''
# rubyDict ={}

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

    def morethanOne(self, nums):
        '''
        複数の処理番号から、ひとつづつ処理する
        :param nums: 　処理番号
        :return:
        '''
        for num in nums:
            print(num)
            self.SourceBase(num)

    def getFile(self, fileNumber):
        '''
        1ファイルのルビ辞書Dictを作成する
        :param fileNumber:
        :return:''
        '''

        # print(fileDic[fileNumber])
        with open(fileDic[fileNumber], 'rt', encoding='utf-8') as file:
            newline_break = ""
            for readline in file:
                line_strip = readline.strip()
                newline_break += line_strip

        (filename, items) = newline_break.split(';')

        line_strip0 = items.replace('{', '').replace('}', '')
        line_strip1 = line_strip0.replace(' ', '', 200)

        if len(line_strip1) == 0:
            return(filename, {})
        else:
            #   Dictデータ取得
            dictItems = line_strip1.split(',')
            kanjiDict = {}
            for term in dictItems:
                # print(term)
                term2 = term.replace(' ', '', 100)
                # print(term2)
                (k, v) = term2.split(':')
                if k is None or v is None:
                    pass
                else:
                    kanjiDict[k] = v

            # print(kanaDict)
            return filename, kanjiDict

    def SourceBase(self, fileNumber):
        filename, kanjiDict = self.getFile(fileNumber)
        # print('filename : ' + filename)
        self.inFile = indir + filename
        self.outFile = outdir + filename

        if kanjiDict == {}:
            shutil.copyfile(self.inFile, self.outFile)
            return(0)

        with open(self.inFile, 'rt', encoding='utf-8') as f:
            originLines = f.readlines()

        fout = open(self.tmpFile, 'wt', encoding='utf-8')

        startFlg = False
        for inLine in originLines:
            newline = inLine
            if startFlg == False:
                # print(new)
                if re.search('<body>', newline):
                    startFlg = True
            else:
                # con=0
                for kanji in kanjiDict.keys():
                    # if con >= CHANGENUM:
                    #     print('con >= CHANGENUM:')
                    #     print(CHANGENUM, con)
                    #     continue

                    if re.search(kanji, newline):

                        if re.search('<rb>*' + kanji + '</rb>', newline) is None\
                                and re.search('<rb>' + kanji + '*</rb>', newline) is None:
                            kana = kanjiDict.get(kanji)
                            newline = re.sub(kanji,
                                         '<ruby> <rb>' + kanji + '</rb> <rp>（</rp> <rt>' + kana + '</rt> <rp>）</rp> </ruby>',
                                         newline)
                            # con += 1
                            # print("yes" + newline, end="")
                            # print(new)
                        else:
                            # print("no" + newline, end="")
                            pass

            fout.write(newline)

        fout.close()
        shutil.copyfile(self.tmpFile, self.outFile)

def go():
    ruby = PutRuby()
    # fnums = [1,2, 3,4,5,7,8,9,10,11,12,30]
    fnums = [3]
    # fnums = [7,8,9,10,11,12,]
    ruby.morethanOne(fnums)
    # ruby.SourceBase(fileNumber=2)

if __name__ == '__main__':

    go()

    sys.exit()
