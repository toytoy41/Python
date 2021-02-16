import sys
import codecs

class ProductKey:
    """
    """

    strPack = '中村君千葉県柏市松葉町'

    def __init__(self):
        # print("Initilized!")
        pass

    def MakeProductKey(self, name, company):
        packeName = name + ProductKey.strPack
        byteName = packeName.encode('Shift-jis')

        i = 0
        productKey = ''

        while (i < len(byteName)) and (i < 8):
            productKey += hex(byteName[i+1])[2:]
            productKey += hex(byteName[i])[2:]

            i = i + 2

        # print (strOut2)
        return productKey.upper()

if __name__ == '__main__':

    company = '協同エンタープライズ'
    name = '鈴木宏治'

    clsPK = ProductKey()
    pcode:str = clsPK.MakeProductKey(name, company)

    print('会社名  = ' + company)
    print('氏名    = ' + name)
    print('プロダクトコード = ' + pcode)

    sys.exit()
