#-*-coding:utf8-*-
# 2018/01/11 创建
# 用于融合视频，视频存于../downloads下
# commands 被subprocess取代
import glob,os,subprocess,logging
from dateutil.parser import parse
from datetime import datetime, timedelta

START_DATE = '20171202'
END_DATE   = '20171208'

def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        return True
    else:
        return False

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='MergeVideoInfoLog.log',
                filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logging.info("start MergeVideo")

# 包含start_date, 包含end_date
start_date = parse(START_DATE)
end_date = parse(END_DATE)

mkdir('~/MergeVideos/xwlb/')


# 融合后下载检查无问题再删原视频
# 合并后视频命名为“20171201.mp4”,路径为 /home/normal/MergeVideos/xwlb/
# 命令为 :
if 0:
    print("ffmpeg -f concat -safe 0 -i ~/xwlb_down/MergeInfo/20171001.txt -c copy ~/MergeVideos/xwlb/20171001.mp4")

for MergeFileInfo in glob.glob(r'MergeInfo/*.txt'):
    file_date = MergeFileInfo.split('.')[0].split('/')[1]
    cur_date = parse(file_date)
    if cur_date >= start_date and cur_date <= end_date:
        output_file_name = ' ~/MergeVideos/xwlb/' + file_date + '.mp4'
        logging.info("DATE: %s, expect output: %s", file_date, output_file_name)
        status, output = subprocess.getstatusoutput('ffmpeg -f concat -safe 0 -i %s -c copy %s'%(MergeFileInfo,output_file_name))
        logging.info("DATE: %s RESULT: "%file_date + str(status) + "\n\n")
        logging.debug(output)


    
