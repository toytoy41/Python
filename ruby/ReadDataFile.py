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
           26:'KOrikomi.txt', 27:'KFront.txt'}

#　42，43，44　は　41に含まれる
#　30はルビなし
def getData(numbers):
    '''
    fileDicから必要な
    :param numbers:
    :return:
    '''
    for i in numbers:
        getFile(i)

def getFile(fileNumber):
    '''
    1ファイルのルビ辞書Dictを作成する
    :param fileNumber:
    :return:
    '''

    with open(fileDic[fileNumber], 'rt', encoding='utf-8') as file:
        newline_break = ""
        for readline in file:
            line_strip = readline.strip()
            newline_break += line_strip

    (k, v) = newline_break.split(';')

    line_strip0 = v.replace('{', '').replace('}', '')
    line_strip1 = line_strip0.replace(' ', '', 200)
    print(k)
    print(line_strip1)

    line_strip2 = line_strip1.split(',')

    newDict = {}
    for term in line_strip2:
        # print(term)
        term2 = term.replace(" ", '', 100)
        # print(term2)
        (k2, v2) = term2.split(':')
        newDict[k2] = v2

    print(newDict)
    return (newDict)

