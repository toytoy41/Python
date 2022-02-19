import sys
import re
import shutil
from data import option_dict

fileDic = {1: 'K0.txt', 2: 'K10.txt', 3: 'K11.txt', 4: 'K12.txt', 5: 'K121.txt',
           6: 'K122.txt', 7: 'K123.txt', 8: 'K21.txt', 9: 'K211.txt', 10: 'K212.txt',
           11: 'K22.txt', 12: 'K23.txt', 13: 'K30.txt', 14: 'K31.txt', 15: 'K32.txt',
           16: 'K41.txt', 17: 'K42.txt', 18: 'K43.txt', 19: 'K44.txt', 20: 'K51.txt',
           21: 'K52.txt', 22: 'K61.txt', 23: 'K62.txt', 24: 'K71.txt', 25: 'K72.txt',
           26: 'KOrikomi.txt', 27: 'KFront.txt', 30: 'nav.html'}
# fileDic = {1:'K0.txt', 2:'K10.txt', 3:'K11.txt', 4:'K12.txt', 5:'K121.txt',
#            6:'K122.txt', 7:'K123.txt', 8:'K21.txt', 9:'K211.txt', 10:'K212.txt',
#            11:'K22.txt', 12:'K23.txt', 14:'K31.txt', 15:'K32.txt',
#            16:'K41.txt', 20:'K51.txt',
#            21:'K52.txt', 22:'K61.txt', 23:'K62.txt', 24:'K71.txt', 25:'K72.txt',
#            26:'KOrikomi.txt', 27:'KFront.txt', 30:'nav.txt'}

indir = './in/'
outdir = './out/'
# originLines = ''
# inFile = ''
# outFile = ''
tmpFile = 'tmp.html'
# file_data = {}
# file_do = []
# file_dont = []
data_dir = './data/'
# file_name = ''


class PutRuby():
    global file_name
    global kanji_dict
    # global my_options
    global do_donot
    global NAK

    def __init__(self):
        file_name = ''
        kanji_dict = {}
        # my_options = {}
        do_donot = {}
        NAK = False

        pass

    def morethan_one(self, nums):
        for num in nums:
            self.source_base(num)

    def source_base(self, fileNumber):

        file_name, kanji_dict, options = self.get_dict(fileNumber)
        processed_num = self.clear_proccess_cnt_disc(options)

        in_file = indir + file_name
        out_file = outdir + file_name

        if kanji_dict == {}:    # ルビデータがなければ、そのままコピー
            shutil.copyfile(in_file, out_file)
            return (0)

        with open(in_file, 'rt', encoding='utf-8') as f:
            originLines = f.readlines()
        fout = open(tmpFile, 'wt', encoding='utf-8')

        through = False     #   True でルビ付けをしない
        start_flg = False  # <body>　データまでは無条件で書き出す

        for inLine in originLines:  # オリジナルデータを一行づつ処理
            newline = inLine
            if start_flg == False:
                if re.search('<body>', newline) or NAK == True:
                    start_flg = True
            else:
                for kanji in kanji_dict:
                    '''
                    入力行に対して、辞書をしらべて、該当する単語があれば、ルビをフル
                    '''

                    through = False
                    # option = False            #   オプション処理があるか
                    escape_flag = False  # 処理した
                    do, dont = self.get_do_dont(options, kanji)

                    if re.search(kanji, newline):
                        if dont != {}:  # この漢字にはoption処理がある
                            '''
                            この行に、例外文字列があれば、一時タグ<toy>で囲っておく
                            '''
                            for notstr in dont:  # don't処理; 当該もじを<toy>タグで囲む
                                escape_flag = True  # この行はオプション処理をする
                                newline = re.sub(notstr, '<toy>' + notstr + '</toy>', newline)
                                '''
                                この行に例外処理文字列がなければ、なにもしない。
                                '''

                        protect_flag = False
                        if re.search('<toy>.*' + kanji + '</toy>', newline):
                            protect_flag = True
                            # print('1 ' + kanji)
                        if re.search('<toy>' + kanji + '.*</toy>', newline):
                            protect_flag = True
                            # print('2 ' + kanji)
                        if re.search('<rb>.*' + kanji + '</rb>', newline):
                            protect_flag = True
                            # print('3 ' + kanji)
                        if re.search('<rb>' + kanji + '.*</r>', newline):
                            protect_flag = True
                            # print('4 ' + kanji)

                        ok = False  # 書いてよい。この漢字は幾つ目？
                        if protect_flag == False:  # 問題ないから、ルビをフル
                            # print(kanji)
                            # print(do)

                            if do != []:
                                if processed_num[kanji] == -1:
                                    through = True
                                    continue

                                # print(kanji)
                                # print(do)
                                splitted = newline.split(kanji)
                                kanji_num = len(splitted) - 1  # この行にある該当漢字の個数

                                cnt = processed_num[kanji]

                                i = 1
                                while i <= kanji_num:
                                    cnt = cnt + 1
                                    if cnt in do:
                                        ok = True
                                    i += 1

                                # print('{} {} {}'.format(repeat_num, cnt,do))
                                if cnt > max(do):
                                    processed_num[kanji] = -1
                                    through = True
                                    # print('over >>> {} {} {}'.format(repeat_num, cnt, do))
                                else:
                                    processed_num[kanji] = processed_num[kanji] + kanji_num

                            else:
                                ok = True

                        if ok == True and through == False:
                            # print(kanji)
                            kana = kanji_dict[kanji]
                            newline = re.sub(kanji,
                                             '<ruby> <rb>' + kanji + '</rb> <rp>（</rp> <rt>' + kana + '</rt> <rp>）</rp> </ruby>',
                                             newline)
                        else:
                            pass

                        if escape_flag == True:
                            newline = re.sub('<toy>', '', newline)
                            newline = re.sub('</toy>', '', newline)

            fout.write(newline)

        fout.close()
        shutil.copyfile(tmpFile, out_file)

    def get_dict(self, fileNumber):
        # global file_name,kanji_dict,my_options
        #
        global NAK
        NAK = False

        if fileNumber == 1:
            from WK10 import ruby_dict, options
        elif fileNumber == 2:
            from WK10 import ruby_dict, options
        elif fileNumber == 3:
            from WK11 import ruby_dict, options
        elif fileNumber == 4:
            from WK12 import ruby_dict, options
        elif fileNumber == 5:
            from WK121 import ruby_dict, options
        elif fileNumber == 6:
            from WK122 import ruby_dict, options
        elif fileNumber == 7:
            from WK123 import ruby_dict, options
        elif fileNumber == 8:
            from WK21 import ruby_dict, options
        elif fileNumber == 9:
            from WK211 import ruby_dict, options
        elif fileNumber == 10:
            from WK212 import ruby_dict, options
        elif fileNumber == 11:
            from WK22 import ruby_dict, options
        elif fileNumber == 12:
            from WK23 import ruby_dict, options
        elif fileNumber == 13:
            from WK30 import ruby_dict, options
        elif fileNumber == 14:
            from WK31 import ruby_dict, options
        elif fileNumber == 15:
            from WK32 import ruby_dict, options
        elif fileNumber == 16:
            from WK41 import ruby_dict, options
        elif fileNumber == 17:
            from WK42 import ruby_dict, options
        elif fileNumber == 18:
            from WK43 import ruby_dict, options
        elif fileNumber == 19:
            from WK44 import ruby_dict, options
        elif fileNumber == 20:
            from WK51 import ruby_dict, options
        elif fileNumber == 21:
            from WK52 import ruby_dict, options
        elif fileNumber == 22:
            from WK61 import ruby_dict, options
        elif fileNumber == 23:
            from WK62 import ruby_dict, options
        elif fileNumber == 24:
            from WK71 import ruby_dict, options
        elif fileNumber == 25:
            from WK72 import ruby_dict, options
        elif fileNumber == 26:
            from WKOrikomi import ruby_dict, options
        elif fileNumber == 27:
            from WKFront import ruby_dict, options
        elif fileNumber == 28:
            from WKFront import ruby_dict, options
        elif fileNumber == 30:
            from WKnav import ruby_dict, options
            NAK = True

        # file_name = ruby_dict[0]
        # kanji_dict = ruby_dict[1]
        # my_options = options
        return (ruby_dict[0], ruby_dict[1], options)

    def clear_proccess_cnt_disc(self, options):
        '''
        do データ作成
        :param options:
        :return:
        '''
        global OPTION_FLAG

        if options == {}:
            OPTION_FLAG = False
            return ({})
        else:
            # for kanji in option:
            #     # processed_disc.update({kanji: 0})
            #     processed_disc[kanji] = 0
            OPTION_FLAG = True
            processed_disc = {kanji: 0 for kanji in options}
            return (processed_disc)

    def get_do_dont(self, options, kanji):
        if kanji in options:
            do, dont = options[kanji]
        else:
            do = []
            dont = []
        # print('kanji do {} {}'.format(kanji,do))
        # print('kanji dont {} {}'.format(kanji,dont))
        return (do, dont)

    # def get_max(self, nums):
    #     max = 0
    #     if nums != []:
    #         max = nums[0]
    #         for i in nums:
    #             if max < i:
    #                 max = i
    #     return max

    # def get_file_kanji_option(self, text_num, kanji):
    #     # print('get_file_kanji_option  ' + kanji)
    #
    #     do = []
    #     dont = []
    #     if OPTION == False:
    #         return (do, dont)
    #
    #     if kanji in option_dict[text_num]:
    #         do, dont = option_dict[text_num][kanji]
    #     # print('')
    #     return (do, dont)
    #
    # def get_dict_data(self, fileNumber):
    #     '''
    #     1ファイルのルビ辞書Dictを作成する
    #     :param fileNumber:
    #     :return:''
    #     '''
    #
    #     # print(fileDic[fileNumber])
    #     with open(data_dir + fileDic[fileNumber], 'rt', encoding='utf-8') as file:
    #         newline_break = ""
    #         for readline in file:
    #             line_strip = readline.strip()
    #             newline_break += line_strip
    #     # print(newline_break)
    #     (filename, items) = newline_break.split(';')
    #
    #     line_strip0 = items.replace('{', '').replace('}', '')
    #     line_strip1 = line_strip0.replace(' ', '', 200)
    #
    #     if len(line_strip1) == 0:  # ルビデータがない
    #         return (filename, {})
    #     else:
    #         #   Dictデータ取得
    #         dictItems = line_strip1.split(',')
    #         kanjiDict = {}
    #         for term in dictItems:  # ルビデータをDictに収集
    #             # print(term)
    #             term2 = term.replace(' ', '', 100)
    #             # print(term2)
    #             (k, v) = term2.split(':')
    #             if k is None or v is None:
    #                 pass
    #             else:
    #                 kanjiDict[k] = v
    #
    #         return filename, kanjiDict

    # def get_file_option(self, text_num):
    #     '''
    #     ファイルにoptionがあれば、optionデータを返す
    #     なければ、{}を返す
    #     :param text_num:
    #     :return:
    #     '''
    #     if text_num in option_dict:
    #         # print(option_dict[text_num])
    #         return (option_dict[text_num])
    #     else:
    #         return {}


def go():
    ruby = PutRuby()

    # fnums = [1,2, 3,4,5,6,7,8,9,10,11,12,13,14,15]
    # fnums = [16,17, 18,19,20,21,22,23,24,25]
    fnums = [9]
    # fnums = [30]
    ruby.morethan_one(fnums)


if __name__ == '__main__':
    go()

    sys.exit()
