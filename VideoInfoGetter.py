# coding: utf-8
import pickle
import json
import threading
import logging
import time
import random
import requests
# 2018.01.10 加入日志，多线程, 代理

# 配置信息
NUM_THREADS = 5
videoid_file_path = 'VideoId/videoid-20161231-20171231.pkt'
VIDEOS_PER_FILE = 30 
proxies = []
with open('proxies.pkt', 'rb') as pro_file:
    proxies = pickle.load(pro_file)
proxies_size = len(proxies)


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

# Read VideoId dictionary
videoid_dic = None
with open(videoid_file_path, 'rb') as videoid_file:
    videoid_dic = pickle.load(videoid_file)   

dic_size = len(videoid_dic.keys())

# 线程池
thread_pool = []
# 线程锁
thread_locks = []

# test_keys={'20170101','20170601'}
# t_videoid_dic={ key:value for key,value in videoid_dic.items() if key in test_keys}
# # print(t_videoid_dic)
# dic_size = len(t_videoid_dic.keys(

# 将下载链接分成若干个文件，每个下载链接文件有VIDEOS_PER_FILE个
# 获取信息
def getInfo(date, vid):
    # 随机用一个代理，或不用代理
    # vid = 'e3b0ffff76444ecdbebfd791d5df09e2'
    # videoid='df67ad75ab4044b0b7a9875c43ba2051'
    url='http://115.182.34.168/api/getHttpVideoInfo.do?pid=%s&from=cbox'%vid
    proxy_id = random.randint(-1,len(proxies)-1)
    if proxy_id == -1:
        req = requests.get(url='%s' % (url))
    else:
        req = requests.get(url='%s' % (url), proxies = proxies[proxy_id])
    res = req.content
    res = res.decode(encoding='utf-8') 
    dic_res = json.loads(res)
    logging.info("get info of video date = %s, vid = %s"%(date,vid))
    return dic_res

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

def InfoProcesser(index, sub_dic):
    # 上锁
    thread_locks[index].acquire()
    urls = []
    dic_size = len(sub_dic.keys())
    for date_index, date in enumerate(sub_dic.keys()):
        dic_res = getInfo(date, sub_dic[date])
        try:
            links = dic_res['video']['chapters4']
            urls += links
            writeMergeFile(date, links)
            # 写入下载文件
            if (date_index == dic_size - 1) or (date_index != 0 and date_index % VIDEOS_PER_FILE) == 0:
                writeDownFile(date, urls)
                urls = []
        except Exception as e:
            logging.warn(str(e)+' Video [date=%s, vid=%s]'%(date, sub_dic[date]))
    # 解锁
    thread_locks[index].release()

# 将视频分配到各个线程
dic_list = []
for i in range(NUM_THREADS):
    sub_dic={}
    dic_list.append(sub_dic)
 
for date_index, date in enumerate(videoid_dic.keys()):
    belongging_thread = date_index % NUM_THREADS
    dic_list[belongging_thread][date] = videoid_dic[date]

# 创建线程
for i in range(NUM_THREADS):
    t1 = threading.Thread(target=InfoProcesser, args=(i, dic_list[i]), name = 'thread-' + str(i))
    thread_pool.append(t1)
    thread_locks.append(threading.Lock())

# 启动线程
for i in range(NUM_THREADS):
    thread_pool[i].start()
    logging.info('thread-'+str(i)+' is start')

# 待线程创建完毕  
time.sleep(5)

# 检查线程是否完成
for i in range(NUM_THREADS):
    thread_locks[i].acquire()
    logging.info('thread-'+str(i)+' is over')
