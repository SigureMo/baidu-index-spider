import requests
import json
import os
import time
import re
import random

from urllib import parse
from bs4 import BeautifulSoup
from PIL import Image
import PIL.ImageOps

from baidulogin import login,getcookies
from siguretools.network_file import Networkfile
from siguretools.config import Config
class BaiduIndex2():
    def __init__(self,words,driver):
        #初始化words
        for n in range(len(words)):
            words[n]=parse.quote(words[n].encode('gb2312'))
        self.words=words
        #初始化driver
        self.driver=driver
        self.driver.get('http://index.baidu.com/?tpl=trend&word='+'%2C'.join(self.words))
        #初始化res、res2
        self.res=self.driver.execute_script('return PPval.ppt;')
        self.res2=self.driver.execute_script('return PPval.res2;')
        #初始化cookies
        try:
            with open('data/cookies.json','rb') as c:
                self.cookies=json.loads(c.read().decode())
        except:
            self.cookies=getcookies(DEBUG)
        cook_str=[]
        for cookie in self.cookies:
            cook_str.append(cookie.get('name')+'='+cookie.get('value'))
        cook_str='; '.join(cook_str)
        self.headers={
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'index.baidu.com',
            'Referer': 'https://index.baidu.com/?tpl=trend&type=0&area=0&time=13&word=''%2C'.join(self.words),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie':cook_str,
            }
        self.indexes=[]

    def getIndex(self,startdate,enddate):
        startdate_stamp=time.mktime(time.strptime(startdate,'%Y-%m-%d'))
        endtime_stamp=time.mktime(time.strptime(enddate,'%Y-%m-%d'))
        if endtime_stamp-startdate_stamp==60*60*24*(30-1):
            self.classType='2'
            url='http://index.baidu.com/Interface/Search/getALLIndex/'
        else:
            self.classType='1'
            url='http://index.baidu.com/Interface/Search/getSubIndex/'
        params={
            'res':self.res,
            'res2':self.res2,
            'startdate':startdate,
            'enddate':enddate,
            }
        response=requests.get(url,headers=self.headers,params=params).json()
        self.skey=response.get('data').get('skey')
        for num in range(len(response.get('data').get('all'))):
            data={}
            data['key']=response.get('data').get('all')[num].get('key')
            data['period']=response.get('data').get('all')[num].get('period')
            data['area']=response.get('data').get('all')[num].get('area')#区域
            data['areaName']=response.get('data').get('all')[num].get('areaName')
            for t in ['all','pc','wise']:
                data[t+'_res3_agv_w']=response.get('data').get(t)[num].get('ratio').get('agv_w_enc')
                data[t+'_res3_agv_m']=response.get('data').get(t)[num].get('ratio').get('agv_m_enc')
                data[t+'_res3_agv']=response.get('data').get(t)[num].get('userIndexes_avg_enc')
                data[t+'_res3s']=response.get('data').get(t)[num].get('userIndexes_enc').split(',')
            self.indexes.append(data)
    
    def getIndexShow(self,res3s):
        url='http://index.baidu.com/Interface/IndexShow/show/?res={}&res2={}&classType={}'.format(self.res,self.res2,self.classType)
        for res3 in res3s:
            url+='&res3[]='+res3
        if self.classType=='1':
            url+='&className=view-value&'+str(int(time.time()*1000))
        elif self.classType=='2':
            url+='&className=profWagv'
        response=requests.get(url,headers=self.headers).json()
        #time.sleep(0.5)
        return response
            
    def getImage(self,res3s):
        def joint(file,imgs_params):
            imgs=[]
            master_map=Image.open(file)
            if self.classType=='1':
                master_map=recolor(master_map)
            hight=master_map.size[1]
            for imgnum in range(len(imgs_params)):
                params=imgs_params[imgnum]
                target=Image.new('RGB',(sum(list(map(lambda x:x[0],params))),hight))
                for num in range(len(params)):
                    region=(params[num][1],0,sum(params[num]),hight)
                    figure=master_map.crop(region)
                    target.paste(figure,(sum(list(map(lambda x:x[0],params[:num]))),0,\
                                         sum(list(map(lambda x:x[0],params[:num+1]))),hight))
                imgname=file[:-4]+'_'+str(imgnum)+'.png'
                imgs.append(target)
                target.save(imgname)
            return imgs

        def recolor(img):
            img=img.convert('RGB')
            width,height=img.size
            for i in range(width):
                for j in range(height):
                    if img.getpixel((i,j))[:3]==(77,77,77):
                        img.putpixel((i,j),(255,255,255))
                    else:
                        img.putpixel((i,j),(77,77,77))
            return img

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

        def img2str(img):
            try:
                im=Image.open(img)
            except:
                im=img
            width=im.size[0]
            hight=im.size[1]
            s=''
            for i in range(width//8):
                region=(i*8,0,(i+1)*8,hight)
                figure=im.crop(region)
                s+=recognition(figure)
            return s

        indexes=[]
        for i in range(len(res3s)//30+1):
            res3s_u=res3s[i*30:(i+1)*30]
            if not res3s_u:
                break
            res3s_u.append(str(random.randint(0,99)))
            styles=self.getIndexShow(res3s_u).get('data').get('code')[:-1]
            url='http://index.baidu.com'+re.search(r'url\("(?P<url>.*)"\)',BeautifulSoup(styles[0],'html.parser').style.string).group('url')
            file='temp/temp'+str(random.randint(0,9999999))+'.png'
            with open(file,'wb') as f:
                f.write(requests.get(url,headers=self.headers).content)
            imgs_params=[]
            for style in styles:
                soup=BeautifulSoup(style,'html.parser')
                imgparams=[]
                for imgval in soup.find_all('span',attrs={'class':'imgval'}):
                    imgparams.append([
                        int(re.search(r'width:(?P<width>\d+)px;',imgval.attrs['style']).group('width')),
                        int(re.search(r'margin-left:-(?P<margin_left>\d+)px;',imgval.div.attrs['style']).group('margin_left'))
                        ])
                imgs_params.append(imgparams)
            for img in joint(file,imgs_params):
                indexes.append(img2str(img).replace(',',''))
        return indexes
        
startdate='2018-01-08'
enddate='2018-07-06'


driver=login('http://index.baidu.com',False)
i=BaiduIndex2(['哈哈','啦啦'],driver)
i.getIndex(startdate,enddate)

indexes=i.getImage([i.indexes[0]['all_res3_agv_w'],i.indexes[1]['all_res3_agv_w']])
print(indexes)

input('Press <Enter>')

