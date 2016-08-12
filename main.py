# -*- coding=utf-8 -*-
__author__ = 'Rocky'
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
            print "IP:%s\tPort:%s" % (t1[0], t1[1])
            if self.isAlive(t1[0], t1[1]):

                self.insert_db(self.now,t1[0],t1[1])
        for i in result_odd:
            t2 = i.xpath("./td/text()")[:2]
            print "IP:%s\tPort:%s" % (t2[0], t2[1])
            if self.isAlive(t2[0], t2[1]):
                self.insert_db(self.now,t2[0],t2[1])


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

    def loop(self,page):
        for i in range(1,page):
            self.getContent(i)

    #查看爬到的代理IP是否还能用
    def isAlive(self,ip,port):
        proxy={'http':ip+':'+port}
        print proxy

        #使用这个方式是全局方法。
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
                print "work"
                return True
            else:
                print "not work"
                return False
        except :
            print "Not work"
            return False


if __name__ == "__main__":
    now = datetime.datetime.now()
    print "Start at %s" % now
    obj=getProxy()
    obj.loop(5)

