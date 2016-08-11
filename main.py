#-*- coding=utf-8 -*-
__author__ = 'xda'
import urllib2,time,datetime
from lxml import etree,html

def getContent(num):

    user_agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
    header={"User-Agent":user_agent}
    url="http://www.xicidaili.com/nn/"+str(num)
    req = urllib2.Request(url,headers=header)
    resp=urllib2.urlopen(req,timeout=10)
    content = resp.read()
    #print content
    et=etree.HTML(content)

    '''
    ip_list1=et.xpath('//td[@class="country"]/following-sibling::*[1]/text()')
    ip_list2=et.xpath('//td[@class="country"]/following-sibling::*[2]/text()')
    ip_list3=et.xpath('//td[@class="country"]/following-sibling::*[5]/text()')

    #print ip_list
    print ip_list1
    print ip_list2
    print ip_list3
    '''
    '''
    for i in ip_list1:
      #print type(i)
      print i
      print "*"
    '''

    #doc=et.xpath('//div/table[@id="ip_list"]/tr/td/text()')
    '''
    k=0
    for i in doc:

      print i
      print k
      k=k+1
    '''

    '''
    print doc
    ip_list=[]
    for i in range(1,100):
      proxy=doc[i*10]+":"+doc[i*10+1]
      ip_list.append(proxy)

    print ip_list
    '''

    result_even=et.xpath('//tr[@class=""]')
    result_odd=et.xpath('//tr[@class="odd"]')
    #print result
    for i in result_even:
      print i.xpath("./td/text()")[:2]
      print "*"*20
    for i in result_odd:
      print i.xpath("./td/text()")[:2]
      print "*"*20
if __name__=="__main__":
    now=datetime.datetime.now()
    print "Start at %s" %now
    num=1
    getContent(num)
