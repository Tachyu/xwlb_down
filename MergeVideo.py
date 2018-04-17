#-*-coding:utf8-*-
# 2018/01/11 创建
# 用于融合视频，视频存于../downloads下
# commands 被subprocess取代
import glob,os,subprocess,logging,time,sys, coloredlogs, getopt
from dateutil.parser import parse
from datetime import datetime, timedelta

coloredlogs.install()

#  python3 MergeVideo.py -s 20171224 -e 20171231
START_DATE = ''
END_DATE   = ''

# 获取参数
if len(sys.argv) < 2:
    print ('MergeVideo.py -s <Start Date> -e <End Date>')
    sys.exit()

try:
    opts, args = getopt.getopt(sys.argv[1:],"hs:e:",["start=","end="])
except getopt.GetoptError:
    print ('MergeVideo.py -s <Start Date> -e <End Date>')
    sys.exit()
for opt, arg in opts:
    if opt == '-h':
        print ('MergeVideo.py -s <Start Date> -e <End Date>')
        sys.exit()
    elif opt in ("-s", "--start"):
        START_DATE = arg
    elif opt in ("-e", "--end"):
        END_DATE = arg


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
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logging.info("start MergeVideo")

# 包含start_date, 包含end_date
start_date = parse(START_DATE)
end_date = parse(END_DATE)

mkdir('/home/normal/MergeVideos/xwlb/')


# 融合后下载检查无问题再删原视频
# 合并后视频命名为“20171201.mp4”,路径为 /home/normal/MergeVideos/xwlb/
# 命令为 :
if 0:
    print("ffmpeg -f concat -safe 0 -i /home/xwlb_down/MergeInfo/20171001.txt -c copy /home/MergeVideos/xwlb/20171001.mp4")

def delete_videos(infofile):
    with open(infofile, 'r') as infofile:
        vfiles = infofile.readlines()
    print(" %d files will be deleted: "%len(vfiles))
    delete_files = [dfile.split(' ')[1] for dfile in vfiles]
    delete_files = [dfile[1:-2] for dfile in delete_files]
    for delete_f in delete_files:
        os.remove(delete_f)
    

for MergeFileInfo in glob.glob(r'MergeInfo/*.txt'):
    file_date = MergeFileInfo.split('.')[0].split('/')[1]
    cur_date = parse(file_date)
    if cur_date >= start_date and cur_date <= end_date:
        output_file_name = '/home/normal/MergeVideos/xwlb/' + file_date + '.mp4'
        # status, output = subprocess.getstatusoutput('ffmpeg -f concat -safe 0 -i %s -c copy %s'%(MergeFileInfo,output_file_name))
        # subprocess.Popen.wait()
        command = '''
        ffmpeg -f concat -safe 0 -i %s -c copy %s
        '''%(MergeFileInfo,output_file_name)
        status = subprocess.call(command, shell=True)
        # status = subprocess.call(['ffmpeg', '-f', 'concat', '-safe', '0' ,'-i', MergeFileInfo, '-c' 'copy', output_file_name])
        # check file size
        # isFinished = False
        # while not isFinished:
        #     try:
        #         fsize = os.path.getsize(output_file_name)
        #         isFinished = True
        #     except Exception as e:
        #         print(e)
        #         time.sleep(5)
        #         pass
        fsize = os.path.getsize(output_file_name)
        fsize = fsize/float(1024*1024)
        fsize = round(fsize,2)
        if fsize >= 400:
            logging.info("%s, %s, [SUCCESS], %dMB", file_date, output_file_name, fsize)
            delete_videos(MergeFileInfo)
        else:
            logging.warn("%s, %s, [WARNING], %dMB", file_date, output_file_name, fsize)
        # logging.info(" [SUCCESS] File size=%dMB RESULT: %s", 100, str(status))

        # logging.debug(" "+output)


    
