import urllib
from PIL import Image, ImageFile
import requests
from bs4 import BeautifulSoup
import image

def getimg(link,enname):
    href = "https://wiki.52poke.com"+link
    resimg = requests.get(href)
    soupimg = BeautifulSoup(resimg.text, 'html.parser', )
    images = soupimg.select('img')
    for image in images:
        imgsrc = image.get('data-url')
        imgalt = image.get('alt')
        if str(enname) in str(imgalt):
            imgsrc = "https:" + imgsrc
            return imgsrc

def main():
    flag = 0
    flagname = '妙蛙种子'
    res = requests.get('https://wiki.52poke.com/wiki/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89/%E7%AE%80%E5%8D%95%E7%89%88')
    soup = BeautifulSoup(res.text, 'html.parser', )
    tables = soup.select('table')
    shuzi=0
    for table in tables:
        classname = table.get('class')
        #print(classname)
        if "eplist" in classname:
            trlist = table.select('tr')
            for tr in trlist:
                tdlist = tr.select('td')
                if len(tdlist) == 4:
                    tdch = tdlist[1]
                    tden = tdlist[3]
                    resch = tdch.select('a')
                    resen = tden.select('a')
                    name = resch[0].get('title')
                    enname = resen[0].get('title')
                    link = resen[0].get('href')
                    shuzi=shuzi+1
                    shuchu=str(shuzi)+": ['"+name+"','"+enname+"'],"
                    print(shuchu)
                    if str(name) == str(flagname):
                        flag = 1
                    if flag == 1:
                        imgsrc = getimg(link,enname)
                        #print(link)
                        #print(link)icon_unit_601731
                        #这里的引号里写你想要保存的位置
                        fileSavePath = 'C:/Study/file/'+str(name)+'.png'#下载未改名字原图
                        urllib.request.urlretrieve(imgsrc, fileSavePath)#下载90x90头像图片
                        
                    #print(imgsrc)

main()
