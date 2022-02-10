import re
import shutil

filename= 'Watashitachino_Kashiwa_0.html'
pat = {'章':'しょう','発足':'ほっそく','際':'さい','募集':'ぼしゅう',
       '制定':'せいてい','機':'き','名称':'めいしょう','若潮':'わかしお',
       '記念緑化':'きねんりょっか','一致':'いっち','選':'えら','市政':'しせい','周年':'しゅうねん',
       '広':'ひろ','守':'まも','住':'す','太陽':'たいよう','姿':'すがた','発展':'はってん',
       '象徴':'しょうちょう',
       '資料':'しりょう','様子':'ようす','公共':'こうきょう','農家':'のうか','農':'のう','事':'じ',
       '利用':'りよう','災害':'さいがい','地震':'じしん','伝統':'でんとう','先人':'せんじん',
       '郷土':'きょうど','残':'のこ'} #'農':'のう',

indir = './in/'

shutil.copyfile(indir + filename, 'tmp.html')

for kanji in pat.keys():
    with open('tmp.html', 'rt', encoding='utf-8') as f:
        lineList = f.readlines()

    outlines = ''
    for line in lineList:
        changeflag = False

        if re.search(kanji, line):
            # print(line, end="")
            # print("a")
            if re.search('<rb>' + kanji + '.*</rb>', line):
                print("no" + line, end="")
            else:
                kana = pat.get(kanji)
                new = re.sub(kanji,'<ruby> <rb>' + kanji + '</rb> <rp>（</rp> <rt>' + kana + '</rt> <rp>）</rp> </ruby>',
                       line)
                # print("yes" + line, end="")
                # print('new' + new)

                changeflag = True
                outlines = outlines + new
                # print('outlines:' + outlines)

        if changeflag == False:
            outlines = outlines + line

    with open('tmp.html', 'w', encoding='utf-8') as outf:
        outf.writelines(outlines)

outdir = 'out\\'
outfile = outdir + filename
#
# with open(outfile, 'wt', encoding='utf-8') as outfile:
#     # for l in outlines:
#     #     outfile.write(l)
#     #
#     outfile.writelines(lineList)
shutil.copyfile('tmp.html', outfile)
