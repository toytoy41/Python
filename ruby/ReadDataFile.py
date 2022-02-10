#

fileDic = {1:'K0.txt', 2:'K10.txt', 3:'K11.txt', 4:'K12.txt', 5:'K121.txt',
           6:'K122.txt', 7:'K123.txt', 8:'K21.txt', 9:'K211.txt', 10:'K212.txt',
           11:'K22.txt', 12:'K23.txt', 13:'K30.txt', 14:'K31.txt', 15:'K32.txt',
           16:'K41.txt', 17:'K42.txt', 18:'K43.txt', 19:'K44.txt', 20:'K51.txt',
           21:'K52.txt', 22:'K61.txt', 23:'K62.txt', 24:'K71.txt', 25:'K72.txt',
           26:'KOrikomi.txt', 27:'KFront.txt'}

a = {}

with open(fileDic[1], 'rt', encoding='utf-8') as file:
    newline_break = ""
    for readline in file:
        line_strip = readline.strip()
        newline_break += line_strip

k = newline_break.split(':')[0]
line_strip0 = newline_break.split('{')[1].replace('}','',100)
print(k)
print(line_strip0)

# line_strip0 = v.replace(' ','',100)
line_strip2 = line_strip0.split(',')

b = {}
for term in line_strip2:
    # print(term)
    term2 = term.replace(" ",'', 100)
    # print(term2)
    (v, k)=term2.split(':')
    b[v] = k

print(b)
