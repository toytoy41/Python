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

escapeDic = {3:{'道':[[1,2,5],
                     ['道で', '道じゅん','この道','ある道',
                      '道を','道は','道だ', 'は道', '歩道','国道']],
	        '橋':[[1],['鉄橋','橋を']]}
}

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

    def get_dict(self, num):
        # num = 3
        escapeData = escapeDic[3]
        # print(escapeData)

        for item in escapeData.keys():
            do, notdo = escapeData[item]

    def morethan_one(self, nums):
        '''
        複数の処理番号から、ひとつづつ処理する
        :param nums: 　処理番号
        :return:
        '''
        for num in nums:
            print(num)
            self.source_base(num)

    def get_file(self, fileNumber):
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
        # print(newline_break)
        (filename, items) = newline_break.split(';')

        line_strip0 = items.replace('{', '').replace('}', '')
        line_strip1 = line_strip0.replace(' ', '', 200)

        if len(line_strip1) == 0:   #   ルビデータがない
            return(filename, {})
        else:
            #   Dictデータ取得
            dictItems = line_strip1.split(',')
            kanjiDict = {}
            for term in dictItems:      #   ルビデータをDictに収集
                # print(term)
                term2 = term.replace(' ', '', 100)
                # print(term2)
                (k, v) = term2.split(':')
                if k is None or v is None:
                    pass
                else:
                    kanjiDict[k] = v

            return filename, kanjiDict

    def source_base(self, fileNumber):
        filename, kanji_dict = self.get_file(fileNumber)
        # print(kanji_dict)
        escape_data = escapeDic[fileNumber]

        # print('filename : ' + filename)
        self.inFile = indir + filename
        self.outFile = outdir + filename

        if kanji_dict == {}:    #   ルビデータがなければ、そのままコピー
            shutil.copyfile(self.inFile, self.outFile)
            return(0)

        with open(self.inFile, 'rt', encoding='utf-8') as f:
            originLines = f.readlines()

        fout = open(self.tmpFile, 'wt', encoding='utf-8')

        start_flg = False       #   <body>　データまでは無条件で書き出す
        for inLine in originLines:      #   オリジナルデータを一行づつ処理
            newline = inLine
            if start_flg == False:
                if re.search('<body>', newline):
                    start_flg = True
            else:
                for kanji in kanji_dict.keys():
                    '''
                    入力行に対して、辞書をしらべて、該当する単語があれば、ルビをフル
                    '''

                    option = False      #   オプション処理があるか
                    if kanji in escape_data:
                        '''
                        各ファイルのescape_dataデータの当該漢字について
                        doとdontのリストを取得する
                        '''
                        do, dont = escape_data[kanji]
                        option = True
                        '''
                        do　リストがあるのでオプション処理をする
                        '''

                    if re.search(kanji, newline):
                        if option == True:

                            escape_flag = False
                            for notstr in dont:
                                '''
                                dont 文字列のnotstrが、この行にあれば<toy>タグをつける
                                '''
                                escape_flag = True      #　この行はオプション処理をする
                                newline = re.sub(notstr, '<toy>' + notstr + '</toy>', newline)

                            # print(newline)
                            if re.search('<toy>.*' + kanji + '</toy>', newline):
                                print('1')
                            if re.search('<toy>' + kanji + '.*</toy>', newline):
                                print('2')
                            if re.search('<rb>.*' + kanji + '</rb>', newline):
                                print('3')
                            if re.search('<rb>' + kanji + '.*</r>', newline):
                                print('4')

                        if re.search('<toy>.*' + kanji + '</toy>', newline) is None \
                            and re.search('<toy>' + kanji + '.*</toy>', newline) is None \
                            and re.search('<rb>.*' + kanji + '</rb>', newline) is None \
                            and re.search('<rb>' + kanji + '.*</r>', newline) is None:

                            kana = kanji_dict.get(kanji)
                            newline = re.sub(kanji,
                                         '<ruby> <rb>' + kanji + '</rb> <rp>（</rp> <rt>' + kana + '</rt> <rp>）</rp> </ruby>',
                                         newline)
                        else:
                            pass

                        if option == True and escape_flag == True:
                            newline = re.sub('<toy>', '',  newline)
                            newline = re.sub('</toy>', '', newline)

            fout.write(newline)
            # print(newline)

        fout.close()
        shutil.copyfile(self.tmpFile, self.outFile)
        print('OK')

def go():
    ruby = PutRuby()
    # fnums = [1,2, 3,4,5,7,8,9,10,11,12,30]
    fnums = [3]
    # ruby.get_dict(fnums)
    # fnums = [7,8,9,10,11,12,]
    ruby.morethan_one(fnums)
    # ruby.SourceBase(fnums)

if __name__ == '__main__':

    go()

    sys.exit()
