#_*_coding:utf-8_*_

import sys
import requests
import re
reload(sys)
sys.setdefaultencoding('utf-8')

class ImoocSpider(object):
    def __init__(self):
        print "开始爬取内容..."

    def ChangPage(self,url,totalNum):
        allLink=[]
        for pageNum in range(1,1+totalNum):
            allLink.append(re.sub("\d+","%s"%pageNum,url,re.S))
        return allLink

    def GetSource(self,link):
        return  requests.get(link).text

    def GetEveryClass(self,html):
        return re.findall('<li id=".*?</li>',html,re.S)

    def GetInfo(self,eachInfo):
        info={}
        info["title"]=re.search('title="(.*?)"',eachInfo,re.S).group(1)
        info["content"] = re.search('<p(.*?)>(.*?)</p>', eachInfo, re.S).group(2)
        timeandlevel=re.findall('<em>(.*?)</em>',eachInfo,re.S)
        info["classtime"] =timeandlevel[0]
        info["learnlevel"] =timeandlevel[1]
        return info

    def saveInfo(self,classInfo):
        file=open("info.txt","ab")
        for each in classInfo:
            file.write('title:' + each['title'] + '\n')
            file.write('content:'+each['content']+'\n')
            file.write('classtime:' + each['classtime'] + '\n')
            file.write('learnlevel:' + each['learnlevel'] + '\n')
            file.write('\n\n')

        file.close()


if __name__ =='__main__':
    classInfo = []
    url="http://www.jikexueyuan.com/course/?pageNum=1"
    spider=ImoocSpider()
    allLink=spider.ChangPage(url,20)
    for link in allLink:
        print "正在处理链接 "+link
        html=spider.GetSource(link)
        everyClass=spider.GetEveryClass(html)
        for each in everyClass:
            info=spider.GetInfo(each)
            classInfo.append(info)
    spider.saveInfo(classInfo)

