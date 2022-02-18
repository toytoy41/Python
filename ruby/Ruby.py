import sys
import re
import shutil
from data import option_dict

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

# option_dict = {3:{'道':[[1, 2, 5],
#                        ['道で', '道じゅん','この道','ある道',
#                       '道を','道は','道だ', 'は道', '歩道','国道']],
# 	        '橋':[[1],['鉄橋','橋を']]}
#                }

indir = './in/'
outdir = './out/'
originLines = ''
inFile = ''
outFile = ''
tmpFile = 'tmp.html'
file_data ={}
file_do = []
file_dont = []
data_dir = './data/'
file_name = ''


class PutRuby():
    global file_name
    global kanji_dict
    global my_options
    global do_donot

    def __init__(self):
        file_name = ''
        kanji_dict = {}
        my_options = {}
        do_donot = {}

        pass

    def morethan_one(self, nums):
        for num in nums:
            self.source_base(num)

    def get_dict(self,fileNumber):
        if fileNumber == 1:
            from WK10 import ruby_dict, options
        elif fileNumber ==2:
            from WK10 import ruby_dict, options
        elif fileNumber ==3:
            from WK11 import ruby_dict, options
        elif fileNumber ==4:
            from WK12 import ruby_dict, options
        elif fileNumber ==5:
            from WK121 import ruby_dict, options
        elif fileNumber ==6:
            from WK122 import ruby_dict, options
        elif fileNumber ==7:
            from WK123 import ruby_dict, options
        elif fileNumber ==8:
            from WK21 import ruby_dict, options
        elif fileNumber ==9:
            from WK211 import ruby_dict, options
        elif fileNumber ==10:
            from WK212 import ruby_dict, options
        elif fileNumber ==11:
            from WK22 import ruby_dict, options
        elif fileNumber ==12:
            from WK23 import ruby_dict, options
        elif fileNumber ==13:
            from WK30 import ruby_dict, options
        elif fileNumber ==14:
            from WK31 import ruby_dict, options
        elif fileNumber ==15:
            from WK32 import ruby_dict, options
        elif fileNumber ==16:
            from WK41 import ruby_dict, options
        elif fileNumber ==17:
            from WK42 import ruby_dict, options
        elif fileNumber ==18:
            from WK43 import ruby_dict, options
        elif fileNumber ==19:
            from WK44 import ruby_dict, options
        elif fileNumber ==20:
            from WK51 import ruby_dict, options
        elif fileNumber ==21:
            from WK52 import ruby_dict, options
        elif fileNumber ==22:
            from WK61 import ruby_dict, options
        elif fileNumber ==23:
            from WK62 import ruby_dict, options
        elif fileNumber ==24:
            from WK71 import ruby_dict, options
        elif fileNumber ==25:
            from WK72 import ruby_dict, options
        elif fileNumber ==26:
            from WKOrikomi import ruby_dict, options
        elif fileNumber ==27:
            from WKFront import ruby_dict, options

        file_name = ruby_dict[0]
        kanji_dict = ruby_dict[1]
        my_options = options
        return(file_name, kanji_dict, my_options)

    def source_base(self, fileNumber):

        filename, file_kanji_dict, my_options = self.get_dict(fileNumber)
        do_data = self.make_do_data(my_options)

        inFile = indir + filename
        outFile = outdir + filename

        if file_kanji_dict == {}:    #   ルビデータがなければ、そのままコピー
            shutil.copyfile(inFile, outFile)
            return(0)

        with open(inFile, 'rt', encoding='utf-8') as f:
            originLines = f.readlines()

        fout = open(tmpFile, 'wt', encoding='utf-8')

        start_flg = False               #   <body>　データまでは無条件で書き出す

        for inLine in originLines:      #   オリジナルデータを一行づつ処理
            newline = inLine
            if start_flg == False:
                if re.search('<body>', newline):
                    start_flg = True
            else:
                for kanji in file_kanji_dict.keys():
                    '''
                    入力行に対して、辞書をしらべて、該当する単語があれば、ルビをフル
                    '''

                    # option = False      #   オプション処理があるか
                    escape_flag = False #   処理した
                    do, dont = self.get_do_dont(my_options, kanji)

                    if re.search(kanji, newline):

                        if my_options != {}:
                            # print(option_keys)
                            if kanji in my_options:  #　この漢字にはoption処理がある
                                '''
                                この行に、例外文字列があれば、一時タグ<toy>で囲っておく
                                '''
                                for notstr in dont: #　don't処理; 当該もじを<toy>タグで囲む
                                    escape_flag = True      #　この行はオプション処理をする
                                    newline = re.sub(notstr, '<toy>' + notstr + '</toy>', newline)
                                    '''
                                    この行に例外処理文字列がなければ、なにもしない。
                                    '''

                        protect_flag = False
                        if re.search('<toy>.*' + kanji + '</toy>', newline):
                            protect_flag = True
                            print('1 ' + kanji)
                        if re.search('<toy>' + kanji + '.*</toy>', newline):
                            protect_flag = True
                            print('2 ' + kanji)
                        if re.search('<rb>.*' + kanji + '</rb>', newline):
                            protect_flag = True
                            print('3 ' + kanji)
                        if re.search('<rb>' + kanji + '.*</r>', newline):
                            protect_flag = True
                            print('4 ' + kanji)

                        ok = False      #   書いてよい。この漢字は幾つ目？
                        if protect_flag == False:   #　問題ないから、ルビをフル
                            if kanji in do_data:
                                cnt = do_data[kanji]['num']
                                pos = do_data[kanji]['position']
                                cnt = cnt + 1
                                do_data[kanji]['num'] = cnt

                                # print('{}  {}  {}'.format(kanji , cnt, pos))
                                if cnt in pos:
                                    ok = True
                            else:
                                ok = True

                        if ok == True:
                            kana = file_kanji_dict.get(kanji)
                            newline = re.sub(kanji,
                                             '<ruby> <rb>' + kanji + '</rb> <rp>（</rp> <rt>' + kana + '</rt> <rp>）</rp> </ruby>',
                                         newline)
                        else:
                            pass

                        if escape_flag == True:
                            newline = re.sub('<toy>', '',  newline)
                            newline = re.sub('</toy>', '', newline)

            fout.write(newline)

        fout.close()
        shutil.copyfile(tmpFile, outFile)
        # print('OK')

    def get_max(self, nums):
        max = 0
        if nums != []:
            max = nums[0]
            for i in nums:
                if max < i:
                    max = i
        return max

    def get_dict_data(self, fileNumber):
        '''
        1ファイルのルビ辞書Dictを作成する
        :param fileNumber:
        :return:''
        '''

        # print(fileDic[fileNumber])
        with open(data_dir + fileDic[fileNumber], 'rt', encoding='utf-8') as file:
            newline_break = ""
            for readline in file:
                line_strip = readline.strip()
                newline_break += line_strip
        # print(newline_break)
        (filename, items) = newline_break.split(';')

        line_strip0 = items.replace('{', '').replace('}', '')
        line_strip1 = line_strip0.replace(' ', '', 200)

        if len(line_strip1) == 0:  # ルビデータがない
            return (filename, {})
        else:
            #   Dictデータ取得
            dictItems = line_strip1.split(',')
            kanjiDict = {}
            for term in dictItems:  # ルビデータをDictに収集
                # print(term)
                term2 = term.replace(' ', '', 100)
                # print(term2)
                (k, v) = term2.split(':')
                if k is None or v is None:
                    pass
                else:
                    kanjiDict[k] = v

            return filename, kanjiDict

    def get_file_option(self, text_num):
        '''
        ファイルにoptionがあれば、optionデータを返す
        なければ、{}を返す
        :param text_num:
        :return:
        '''
        if text_num in option_dict:
            # print(option_dict[text_num])
            return (option_dict[text_num])
        else:
            return {}

    def make_do_data(self, option):
        '''
        do データ作成
        :param option:
        :return:
        '''
        global OPTION

        do_dict = {}
        # option = my_options
        # print(option)
        if option == {}:
            OPTION = False
            return ({})
        else:
            OPTION = True

        for kanji in option:
            cnt = {'num': 0}

            do, dont = option[kanji]
            # position = {'position' : do}
            cnt.update({'position': do})

            tmp = {kanji: cnt}
            do_dict.update(tmp)

        return (do_dict)

    def get_file_kanji_option(self, text_num, kanji):
        # print('get_file_kanji_option  ' + kanji)

        do = []
        dont = []
        if OPTION == False:
            return (do, dont)

        if kanji in option_dict[text_num]:
            do, dont = option_dict[text_num][kanji]
        # print('')
        return (do, dont)

    def get_do_dont(self,my_options, kanji):

        do = []
        dont = []
        # print(my_options)
        if kanji in my_options:
            do, dont = my_options[kanji]
        return(do, dont)

def go():
    ruby = PutRuby()
    # ruby.make_file_strict_data(3)
    # ruby.get_file_option(3)
    # ruby.get_option(3,'道')
    # fnums = [1,2, 3,4,5,7,8,9,10,11,12,30]
    fnums = [3]
    # fnums = [7,8,9,10,11,12,]
    ruby.morethan_one(fnums)
    # ruby.source_base(3)

if __name__ == '__main__':

    go()

    sys.exit()
