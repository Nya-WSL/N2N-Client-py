import os
import sys
import time
import json
import yaml
import zipfile
import datetime
from urllib import request

workDir = os.getcwd() + "logs"
# 错误处理
class Mylogpetion():
    def __init__(self):
        import traceback
        import logging
# logging的基本配置
        errorTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')  # 获取错误时间
        logging.basicConfig(
            filename=f'{workDir}\\debug_{errorTime}.txt',              # 当前文件写入位置
            format='%(asctime)s %(levelname)s \n %(message)s',             # 格式化存储的日志格式
            datefmt='%Y-%m-%d %H:%M:%S'
        )
# 写入日志
        logging.debug(traceback.format_exc())

try:
    if os.path.exists('config.local.win.json'): # 读取本地配置
        c = open('config.local.win.json','r', encoding='utf-8')
        text = c.read()
        c.close()
        config = json.loads(text)
    else:
        with open('config.local.win.yml', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

    ConServerUrl = config["server"] # 读取服务器配置

    ZipUrl = ConServerUrl + config['Url']['zipUrl'] # 获取更新包url

# 百分比进度条
    def report(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            s = "\r%5.1f%% %*d / %d" % (percent, len(str(totalsize)), readsofar, totalsize)
            sys.stderr.write(s)
            if readsofar >= totalsize:
                sys.stderr.write("\n")
        else:
            sys.stderr.write("read %d\n" % (readsofar,))

    request.urlretrieve(ZipUrl,"n2n_update_win.zip",report) # 下载更新包

    time.sleep(2)
    os.system("taskkill /F /IM n2n_client.exe")
    os.remove("n2n_client.exe")

# 解压更新包
    Unzip = zipfile.ZipFile("n2n_update_win.zip", mode='r')
    for names in Unzip.namelist():
        Unzip.extract(names, os.getcwd())
    Unzip.close()
    input("update is successful, please press Enter and restart n2n_client.")
    os.remove("n2n_update_win.zip")
    if os.path.exists('config.local.win.json'):
        os.remove("config.local.win.json")
    sys.exit("update is successful")
except:
    Mylogpetion() # 输出log