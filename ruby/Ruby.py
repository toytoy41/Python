import sys
import re
import shutil
from data import option_dict

# fileDic = {1:'K0.txt', 2: 'K10.txt', 3: 'K11.txt', 4: 'K12.txt', 5: 'K121.txt',
#            6: 'K122.txt', 7: 'K123.txt', 8: 'K21.txt', 9: 'K211.txt', 10: 'K212.txt',
#            11: 'K22.txt', 12: 'K23.txt', 13: 'K30.txt', 14: 'K31.txt', 15: 'K32.txt',
#            16: 'K41.txt', 17: 'K42.txt', 18: 'K43.txt', 19: 'K44.txt', 20: 'K51.txt',
#            21: 'K52.txt', 22: 'K61.txt', 23: 'K62.txt', 24: 'K71.txt', 25: 'K72.txt',
#            26: 'KOrikomi.txt', 27: 'KFront.txt', 30: 'nav.html'}

indir = './in/'
outdir = './out/'
tmpFile = 'tmp.html'
data_dir = './data/'


class PutRuby():
  global file_name
  global kanji_dict
  global do_donot

  def __init__(self):
    file_name = ''
    kanji_dict = {}
    do_donot = {}

    pass

  def morethan_one(self, nums):
    for num in nums:
      self.source_base(num)

  def source_base(self, fileNumber):
    global kanji_dict
    # options_flag = False

    file_name, kanji_dict, options = self.get_dict(fileNumber)
    processed_num = self.clear_proccess_cnt_disc(options)

    in_file = indir + file_name
    out_file = outdir + file_name

    if kanji_dict == {}:  # ルビデータがなければ、そのままコピー
      shutil.copyfile(in_file, out_file)
      return (0)

    with open(in_file, 'rt', encoding='utf-8') as f:
      originLines = f.readlines()
    fout = open(tmpFile, 'wt', encoding='utf-8')

    through = False  # True でルビ付けをしない
    start_flg = False  # <body>　データまでは無条件で書き出す
    ato_shori = ''  # ['dont_anything','insert_ruby','I_did']
    for inLine in originLines:  # オリジナルデータを一行づつ処理
      newline = inLine
      if start_flg == False:
        if re.search('<body>', newline):
          start_flg = True
      else:
        for kanji in kanji_dict:
          '''
          入力行に対して、辞書をしらべて、該当する単語があれば、ルビをフル
          '''
          if re.search(kanji, newline):

            options_flag, do, dont = self.get_do_dont(options, kanji)

            if options_flag == True:  # option がない。全部ルビ付け

              # if kanji == '包':
              #   print(f'kanji {kanji} do {do} newline {newline}')

              if dont != []:  # この漢字にはoption処理がある
                '''
                この行に、例外文字列があれば、一時タグ<toy>で囲っておく
                '''
                for notstr in dont:  # don't処理; 当該もじを<toy>タグで囲む
                  newline = re.sub(notstr, '<toy>' + notstr + '</toy>', newline)
                  '''
                  この行に例外処理文字列がなければ、なにもしない。
                  '''
              if do == []:  # この行で該当する漢字にすべてルビをふる
                i_did = False
              else:
                '''
                do == True で
                該当する漢字があれば、変換する
                なければ、なにもしない
                '''
                i_did = False
                if processed_num[kanji] != -1:  # 何もしない ルビをうたない
                  splitted = newline.split(kanji)
                  kanji_num = len(splitted) - 1  # この行にある該当漢字の個数

                  i = 1
                  while i <= kanji_num:

                    processed_num[kanji] += 1
                    if processed_num[kanji] > max(do):  # この漢字ではその後のルビを付けない
                      # print('{} {} {}'.format(kanji, i,kanji_num))
                      while i <= kanji_num:  # この行は残りを修繕しておく
                        splitted[i - 1] += kanji
                        i += 1

                      processed_num[kanji] = -1
                      break
                    else:
                      pos = processed_num[kanji]

                      if pos in do:
                        para = splitted[i - 1] + kanji + splitted[i]
                        '''
                        この漢字の前後パラグラフの中で、
                        この漢字は、ルビタグあるいは臨時の<toy>タグの中ではないか。チェック。
                        これらの中では、ルビ処理をしない。
                        '''
                        protect_flag = self.check_protected(kanji, para)

                        if protect_flag == False:

                          kana = kanji_dict[kanji]
                          splitted[i - 1] = splitted[
                                              i - 1] + '<ruby> <rb>' + kanji + '</rb> <rp>（</rp> <rt>' + kana + '</rt> <rp>）</rp> </ruby>'
                          if kanji == 'ああああ':
                            print(f'pos {pos}')
                            print(splitted)
                            # self.my_print(kanji, processed_num, splitted, newline)
                          i_did = True
                        else:
                          splitted[i - 1] += kanji
                      else:
                        splitted[i - 1] += kanji

                      i += 1

                  if i_did == True:
                    newline = ''.join(splitted)

                else:
                  '''
                   processed_num[kanji] == -1 => ルビをつけない
                   なにもしない。　  ルビをつけない
                  '''
            if options_flag == False or do == []:
              # 　option がない。doがない。　===>　全部、ルビをつける。
              newline = self.insert_ruby(kanji, newline)

            if dont != []:
              if re.search('<toy>', newline):
                newline = re.sub('<toy>', '', newline)
                newline = re.sub('</toy>', '', newline)

      fout.write(newline)

    fout.close()
    shutil.copyfile(tmpFile, out_file)

  def atoshori(self, i, kanji, kanji_num, splitted):
    # 　要検討
    '''
    doの中を探したが、該当番号がなかった
    該当する漢字があったので、ルビをつけた
    この行では以後の処理をしないので、修復しておく
    '''
    while i <= kanji_num:  # この行は残りを修繕しておく
      splitted[i - 1] += kanji
      i += 1

  def my_print(self, kanji, processed_num, splitted, newline):
    print(f'kanji : {kanji} processed_num[kanji] : {processed_num[kanji]} ')
    print(splitted)
    print(newline)
    print()

  def check_protected(self, kanji, paragraph):
    '''
    同一行に'包装'あとから'包'があった場合、後の'包'のチェックで'包装'を見に行く。
    この場合、キャンセルされる。　protect_flag = True になる
    '''
    protect_flag = False
    if re.findall('<toy>.*' + kanji + '</toy>', paragraph):
      protect_flag = True
      # print('1 ' + kanji)
    if re.findall('<toy>' + kanji + '.*</toy>', paragraph):
      protect_flag = True
      # print('2 ' + kanji)
    if re.findall('<rb>.*' + kanji + '</rb>', paragraph):
      protect_flag = True
      # print('3 ' + kanji)
    if re.findall('<rb>' + kanji + '.*</r>', paragraph):
      protect_flag = True
      # print('4 ' + kanji)
    return (protect_flag)

  def insert_ruby(self, kanji, newline):
    global kanji_dict

    protect_flag = self.check_protected(kanji, newline)

    if protect_flag == True:
      return newline
    else:
      kana = kanji_dict[kanji]
      newline = re.sub(kanji,
                       '<ruby> <rb>' + kanji + '</rb> <rp>（</rp> <rt>' + kana + '</rt> <rp>）</rp> </ruby>',
                       newline)
      return (newline)

  def get_dict(self, fileNumber):
    # global file_name,kanji_dict,my_options
    #
    # global options
    ruby_dict = []
    options = {}

    if fileNumber == 1:
      from WK0 import ruby_dict, options
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

    file_name = ruby_dict[0]
    kanji_dict = ruby_dict[1]
    myoptions = options
    return (file_name, kanji_dict, myoptions)

  def clear_proccess_cnt_disc(self, options):
    '''
    processed_disc : do リストから、該当漢字が今幾つ処理されたいるか、データを保存
    これを初期化する
    :param options:
    :return:
    '''

    if options == {}:
      return ({})
    else:
      processed_disc = {kanji: 0 for kanji in options}
      return (processed_disc)

  def get_do_dont(self, options, kanji):

    options_flag = False
    do = []
    dont = []

    if kanji in options:
      do, dont = options[kanji]
      options_flag = True
    else:
      options_flag = False

    # print('kanji do {} {}'.format(kanji,do))
    # print('kanji dont {} {}'.format(kanji,dont))
    return (options_flag, do, dont)

    #
    # if OPTION == False:
    #     return (do, dont)
    # if OPTION == False:
    #     return (do, dont)
    #
    # if kanji in options:
    #     do, dont = options[kanji]
    #     # print('')
    # return (do, dont)


def go():
  ruby = PutRuby()
  # fileDic = {1:'K0.txt', 2: 'K10.txt', 3: 'K11.txt', 4: 'K12.txt', 5: 'K121.txt',
  #            6: 'K122.txt', 7: 'K123.txt', 8: 'K21.txt', 9: 'K211.txt', 10: 'K212.txt',
  #            11: 'K22.txt', 12: 'K23.txt', 13: 'K30.txt', 14: 'K31.txt', 15: 'K32.txt',
  #            16: 'K41.txt', 17: 'K42.txt', 18: 'K43.txt', 19: 'K44.txt', 20: 'K51.txt',
  #            21: 'K52.txt', 22: 'K61.txt', 23: 'K62.txt', 24: 'K71.txt', 25: 'K72.txt',
  #            26: 'KOrikomi.txt', 27: 'KFront.txt', 30: 'nav.html'}

  # fnums = [1,2, 3,4,5,6,7,8,9,10,11,12,13,14,15]
  fnums = [16,17, 18,19,20,21,22,23,24,25]
  # fnums = [11]    # 21日まで
  # fnums = [1,2, 3,4,5,6,7,8,9,10,11]
  # fnums = [30]　
  # fnums = [25]

  ruby.morethan_one(fnums)


if __name__ == '__main__':
  go()

  sys.exit()
