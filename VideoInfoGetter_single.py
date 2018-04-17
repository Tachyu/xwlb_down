# coding: utf-8
from urllib import request
import pickle
import logging
import json
VIDEOS_PER_FILE = 30

# Read VideoId dictionary
videoid_file_path = 'VideoId/videoid-20161231-20171231.pkt'
videoid_file=open(videoid_file_path,'rb')    
videoid_dic = pickle.load(videoid_file)    
videoid_file.close()

dic_size = len(videoid_dic.keys())

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='VideoInfoLog.log',
                filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logging.info("start VideoInfoGetter")
# test_keys={'20170101','20170601'}
# t_videoid_dic={ key:value for key,value in videoid_dic.items() if key in test_keys}
# # print(t_videoid_dic)
# dic_size = len(t_videoid_dic.keys())

# 将下载链接写入文件
def writeDownFile(file_index, links):
    filename = 'DownUrls/DF_%d.txt'%file_index
    with open(filename, 'w') as url_down_file:
        links = [link['url'] + "\n" for link in links]
        url_down_file.writelines(links)
    logging.info('Download file: ' + filename + ' is generated.')

# 将视频合并信息写入文件
def writeMergeFile(date, links):
    filename = 'MergeInfo/' + date + '.txt'
    with open(filename, 'w') as merge_file:
        filenames = ["file " + url['url'].split('/')[-1] + '/n' for url in links]
        merge_file.writelines(filenames)
    logging.info('Merge file: ' + filename + ' is generated.')

count = 0
down_urls = []
down_file_count = 0
for date in videoid_dic.keys():
# for date in t_videoid_dic.keys():  
    vid = videoid_dic[date]  
    # vid = t_videoid_dic[date]      
    print('[%d / %d] Current Date: %s'%(count+1, dic_size, date))
    # vid = 'e3b0ffff76444ecdbebfd791d5df09e2'
    # videoid='df67ad75ab4044b0b7a9875c43ba2051'
    url='http://115.182.34.168/api/getHttpVideoInfo.do?pid=%s&from=cbox'%vid
    req = request.Request(url='%s' % (url))
    res = request.urlopen(req)
    res = res.read()
    res = res.decode(encoding='utf-8')
    dic_res = json.loads(res)
    try:
        durations = dic_res['video']['chapters4']
        writeMergeFile(date, durations)
        down_urls += durations
        if (count == dic_size - 1) or (count != 0 and count % VIDEOS_PER_FILE == 0):    
            writeDownFile(down_file_count, down_urls)        
            down_file_count += 1
            down_urls = []
    except Exception as e:
        print(e)
        logging.warn(' Video [date=%s, vid=%s]'%(date, vid))
    count += 1


