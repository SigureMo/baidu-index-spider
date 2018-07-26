from PIL import Image
from pylab import *
import os
import json

def thumbprint(img):
    im=img.resize((8,14),Image.ANTIALIAS).convert('L')
    pixels = list(im.getdata())
    avg = sum(pixels) / len(pixels)
    return "".join(map(lambda p :"1" if p>avg else "0", pixels))

def recognition(img):
    numfont='0123456789%-,'
    im=Image.open('data/numfont.png')
    hight=im.size[1]        
    try:
        with open('data/numfont.json','rb')as f:
            numfont_dict=json.loads(f.read().decode())
    except:
        numfont_dict={}
        for n in numfont:
            region=(numfont.index(n)*8,0,(numfont.index(n)+1)*8,hight)
            figure=im.crop(region)
            numfont_dict[n]=thumbprint(figure)
        print(numfont_dict)
        with open('data/numfont.json','wb')as f:
            f.write(json.dumps(numfont_dict).encode())
    th=thumbprint(img)
    hamming={}
    for n in numfont_dict:
        hamming[n]=0
        for i in range(len(numfont_dict[n])):
            if th[i]!=numfont_dict[n][i]:
                hamming[n]+=1
    mindis=8*14
    num=''
    for n in hamming:
        if hamming[n]<mindis:
            mindis=hamming[n]
            num=n
    return num

def img2num(file):
    im=Image.open(file)
    width=im.size[0]
    hight=im.size[1]
    s=''
    for i in range(width//8):
        region=(i*8,0,(i+1)*8,hight)
        figure=im.crop(region)
        s+=recognition(figure)
    return s
    
        
print(img2num('temp/temp1734507_0.png'))
