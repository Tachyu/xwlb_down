#-*-coding:utf8-*-
# 2018/01/07 创建

import re
import string
import sys
import os
import random
import time
import urllib
from bs4 import BeautifulSoup
import requests

from dateutil.parser import parse
from datetime import datetime, timedelta

import pickle

class VideoIdProvider:
    start_date = None
    end_date   = None
    driver     = None
    date_url   = 'http://tv.cctv.com/lm/xwlb/day/20180104.shtml'
    entry_url  = 'http://tv.cctv.com/lm/xwlb'

    def __init__(self, start_date=None, end_date=None):
        newest_date = datetime.now() - timedelta(days=1)
        try:
            self.start_date = parse(start_date)
            self.end_date = parse(end_date)
            if self.end_date > newest_date:
                self.end_date = newest_date 
            if self.start_date > self.end_date:
                self.start_date = self.end_date
        except Exception as e:
            self.start_date = newest_date
            self.end_date = newest_date
        print(" Start Date: "+ self.start_date.strftime('%Y-%m-%d'))
        print(" End   Date: "+ self.end_date.strftime('%Y-%m-%d'))
        print(" Total Days: "+ str((self.end_date-self.start_date).days))
        # self.driver = webdriver.PhantomJS()
        # self.driver = webdriver.Chrome()
        

    def get_id(self):
        header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
        # self.driver.get(self.entry_url)
        day_delta = (self.end_date - self.start_date).days
        tar_dates = []
        for i in range(day_delta):
            cur_date = self.end_date - timedelta(days=i)
            tar_dates.append(cur_date.strftime("%Y%m%d"))
        id_dic = {}
        for index, day in enumerate(tar_dates):
            if index != 0 and index % 10 == 0:
                print(day)
                time.sleep(random.randint(3,5))
            rep = requests.get(self.date_url.replace('20180104',day),headers = header,timeout=5)
            bs = BeautifulSoup(rep.text, "html.parser")
            img_url = bs.find_all('img')[0]['src']
            video_id = img_url.split('/')[-1].split('.')[0].split('-')[0]
            id_dic[day] = video_id
        return id_dic


if __name__ == '__main__':
    start_date = '20161231'
    end_date = '20171231'
    dic = VideoIdProvider(start_date, end_date).get_id()
    write_file=open('VideoId/videoid-%s-%s.pkt'%(start_date,end_date),'wb')    
    pickle.dump(dic,write_file,-1)    
    write_file.close()
    print(dic)
