# -*- coding=utf-8 -*-
__author__ = 'Rocky'
import re
import requests
from lxml import etree
import urllib2, time, datetime
from lxml import etree
import sqlite3,time

class getProxy():

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.header = {"User-Agent": self.user_agent}
        self.dbname="proxy.db"
        self.now = time.strftime("%Y-%m-%d")

    def getContent(self, num):
        nn_url = "http://www.xicidaili.com/nn/" + str(num)
        #国内高匿
        req = urllib2.Request(nn_url, headers=self.header)
        resp = urllib2.urlopen(req, timeout=10)
        content = resp.read()
        et = etree.HTML(content)
        result_even = et.xpath('//tr[@class=""]')
        result_odd = et.xpath('//tr[@class="odd"]')
        #因为网页源码中class 分开了奇偶两个class，所以使用lxml最方便的方式就是分开获取。
        #刚开始我使用一个方式获取，因而出现很多不对称的情况，估计是网站会经常修改源码，怕被其他爬虫的抓到
        #使用上面的方法可以不管网页怎么改，都可以抓到ip 和port
        for i in result_even:
            t1 = i.xpath("./td/text()")[:2]
            #print "IP:%s\tPort:%s" % (t1[0], t1[1])
            if self.isAlive(t1[0], t1[1]):
                proxies = {'https': 'https://' + t1[0] + ':' + t1[1]}
                self.check_Proxy_IP(proxies)
                #pass
                #self.insert_db(self.now,t1[0],t1[1])
        for i in result_odd:
            t2 = i.xpath("./td/text()")[:2]
            #print "IP:%s\tPort:%s" % (t2[0], t2[1])
            if self.isAlive(t2[0], t2[1]):
                #pass
                #self.insert_db(self.now,t2[0],t2[1])
                proxies = {'https': 'https://' + t2[0] + ':' + t2[1]}
                self.check_Proxy_IP(proxies)

    def insert_db(self,date,ip,port):
        dbname=self.dbname
        try:
            conn=sqlite3.connect(dbname)
        except:
            print "Error to open database%" %self.dbname
        create_tb='''
        CREATE TABLE IF NOT EXISTS PROXY
        (DATE TEXT,
        IP TEXT,
        PORT TEXT
        );
        '''
        conn.execute(create_tb)
        insert_db_cmd='''
        INSERT INTO PROXY (DATE,IP,PORT) VALUES ('%s','%s','%s');
        ''' %(date,ip,port)
        conn.execute(insert_db_cmd)
        conn.commit()
        conn.close()

    def loop(self,page=5):
        for i in range(1,page):
            self.getContent(i)

    #查看爬到的代理IP是否还能用
    def isAlive(self,ip,port):
        proxy={'http':ip+':'+port}
        #print proxy

        #使用这个方式是全局方法。不推荐
        '''
        proxy_support=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        #使用代理访问腾讯官网，进行验证代理是否有效
        test_url="http://www.qq.com"
        req=urllib2.Request(test_url,headers=self.header)
        try:
            #timeout 设置为10，如果你不能忍受你的代理延时超过10，就修改timeout的数字
            resp=urllib2.urlopen(req,timeout=10)

            if resp.code==200:
                print proxy
                #print "work"
                return True
            else:
                #print "not work"
                return False
        except :
            #print "Not work"
            return False
        '''
        testUrl='members.3322.org/dyndns/getip'
        r=requests.get(url=testUrl,headers=self.header,proxies=proxy)
        code= r.status_code
        print r.text
        print code
        if  code==200:
            print "Proxy ", proxy,'works'
            return True
        else:
            return False


    #查看数据库里面的数据时候还有效，没有的话将其纪录删除
    def check_db_pool(self):
        conn=sqlite3.connect(self.dbname)
        query_cmd='''
        select IP,PORT from PROXY;
        '''
        cursor=conn.execute(query_cmd)
        for row in cursor:
            if not self.isAlive(row[0],row[1]):
                #代理失效， 要从数据库从删除
                delete_cmd='''
                delete from PROXY where IP='%s'
                ''' %row[0]
                print "delete IP %s in db" %row[0]
                conn.execute(delete_cmd)
                conn.commit()

        conn.close()

    def getHTTPS(self):
        for i in range(1,5):
            url='http://www.xicidaili.com/wn/%s' %i
            s=requests.get(url,headers=self.header)
            print s
            content = s.text
            et = etree.HTML(content)
            result_even = et.xpath('//tr[@class=""]')
            result_odd = et.xpath('//tr[@class="odd"]')
            # 因为网页源码中class 分开了奇偶两个class，所以使用lxml最方便的方式就是分开获取。
            # 刚开始我使用一个方式获取，因而出现很多不对称的情况，估计是网站会经常修改源码，怕被其他爬虫的抓到
            # 使用上面的方法可以不管网页怎么改，都可以抓到ip 和port
            for i in result_even:
                t1 = i.xpath("./td/text()")[:2]
                # print "IP:%s\tPort:%s" % (t1[0], t1[1])
                if self.isAlive(t1[0], t1[1]):
                    # pass
                    #self.insert_db(self.now, t1[0], t1[1])
                    proxies={'https':'https://'+t1[0]+':'+t1[1]}
                    self.check_Proxy_IP(proxies)
            for i in result_odd:
                t2 = i.xpath("./td/text()")[:2]
                # print "IP:%s\tPort:%s" % (t2[0], t2[1])
                if self.isAlive(t2[0], t2[1]):
                    # pass
                    #self.insert_db(self.now, t2[0], t2[1])
                    proxies={'https':'https://'+t2[0]+':'+t2[1]}
                    self.check_Proxy_IP(proxies)

            print "*"*10


    def getFrom_89vip(self):
        url='http://www.89ip.cn/tiqv.php?sxb=&tqsl=30&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1'
        s=requests.get(url,headers=self.header)
        print s.status_code
        #print s.text
        res=re.findall('<BR>(.*?)<BR>',s.text)

        for i in res:

            #print i
            proxies={'http':'http://'+str(i)}
            print proxies
            self.check_Proxy_IP(proxies)

    def apiDemo(self):
        url='http://api.xicidaili.com'
        s=requests.get(url,headers=self.header)
        print s.status_code
        #print s.text

    def validation(self):
        fp = open('proxy.cfg', 'r')
        lines=fp.readlines()
        print lines
        new_lines=[]
        for i in lines:
            x=eval(i.strip())
            print x
            s = requests.get(url='https://guyuan.anjuke.com/community/p1/', headers=self.header, proxies=x, timeout=10)
            print s.status_code
            if s.status_code == 200:
                new_lines.append(i)

        fp.close()
        new_lines=list(set(new_lines))
        with open('proxy.cfg','w') as fp:
            for i in new_lines:
                fp.write(i)



    def check_Proxy_IP(self,proxies):
        #proxies={'http': '180.105.126.75:8118'}
        #proxies={'https': 'https://112.246.37.48:8118',}
        fp=open('proxy.cfg','a')

        try:
            s=requests.get(url='https://m.lianjia.com/',headers=self.header,proxies=proxies,timeout=10)
            print s.status_code
            if s.status_code==200:
                print str(proxies)
                fp.write(str(proxies))
                fp.write('\n')
                fp.close()
            content=s.text

            p = re.compile(u'请输入图片中的验证码')
            if p.findall(content):
                print "需要手动输入验证码"
                return 404
        except Exception,e:
            print e

        #s=requests.get(url='http://ip.chinaz.com/',headers=self.header)
        #x=etree.HTML(s.text)
        #l=x.xpath('.//p[@class="getlist pl10"]/text()')
        #print l


if __name__ == "__main__":
    now = datetime.datetime.now()
    print "Start at %s" % now

    obj=getProxy()
    #obj.getFrom_89vip()
    obj.getHTTPS()
    #obj.validation()
    #obj.apiDemo()
    #obj.loop()
    #obj.getHTTPS()
    #obj.loop(5)
    #obj.check_db_pool()
    #obj.check_Proxy_IP()
