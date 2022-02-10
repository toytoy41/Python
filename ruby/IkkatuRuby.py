import re

# filename= 'Watashitachino_Kashiwa_0.html'
# pat = {'公共':'こうきょう','農家':'のうか','農':'のう','様子':'ようす'} #'農':'のう',

rubyDict = {
    'Watashitachino_Kashiwa_0.html' :
    {'公共':'こうきょう','農家':'のうか','農':'のう','様子':'ようす'},
    'Watashitachino_Kashiwa_1-0.html' :
        {}
}
fileDic = {1:'K0.txt', 2:'K10.txt', 3:'K11.txt', 4:'K12.txt', 5:'K121.txt',
           6:'K122.txt', 7:'K123.txt', 8:'K21.txt', 9:'K211.txt', 10:'K212.txt',
           11:'K22.txt', 12:'K23.txt', 13:'K30.txt', 14:'K31.txt', 15:'K32.txt',
           16:'K41.txt', 17:'K42.txt', 18:'K43.txt', 19:'K44.txt', 20:'K51.txt',
           21:'K52.txt', 22:'K61.txt', 23:'K62.txt', 24:'K71.txt', 25:'K72.txt',
           26:'KOrikomi.txt', 27:'KFront.txt'}

indir = './in/'
outdir = './out/'

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
