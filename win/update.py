import os
import sys
import time
import json
import zipfile
import logging
import traceback
from urllib import request

try:
# 读取本地配置
    c = open('config.local.win.json','r')
    text = c.read()
    c.close()
    config = json.loads(text)

    LogFile = config['Path']['updateLog'] # 读取log配置

    logging.basicConfig(filename=LogFile,level=logging.DEBUG,format="%(asctime)s - %(pathname)s - %(message)s",datefmt="%Y/\
%m/%d %H:%M:%S") # log配置

    ConServerUrl = config["server"] # 读取服务器配置

    ZipUrl = ConServerUrl + config['Path']['zipUrl'] # 获取更新包url

# 定义Bat脚本路径
    BatRes = config['Path']['batRes']
    Bat = os.getcwd() + BatRes

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
    sys.exit("update is successful")
except:
    logging.debug(traceback.format_exc()) # 输出log