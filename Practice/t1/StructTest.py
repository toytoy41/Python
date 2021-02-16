import struct
from matplotlib.image import imread

# fin = open('./dataset/O_logo.png','rb')
fin = open('./dataset/O\'Reilly_logo.png','rb')
bdata = fin.read()
len(bdata)

print(len(bdata))
# img = imread('../dataset/O\'Reilly_logo.png') # 画像の読み込み

valid_png_header = b'\x89PNG\r\n\x1a\n'

if bdata[:8] == valid_png_header:
    width, height = struct.unpack('>LL', bdata[16:24])
    print('Valid PNG, width', width, 'height', height)