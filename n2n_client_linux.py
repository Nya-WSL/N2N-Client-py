import os
import csv
import sys
import time
import logging
#import zipfile
import requests
import traceback
from urllib import request
from configparser import ConfigParser

# 读取本地配置
ConServer = ConfigParser()
ConServer.read('config.local.linux.ini')

ConServerUrl = ConServer.get('Server','server') # 读取服务器配置

# 服务器列表获取url和临时保存路径
CsvUrl = ConServerUrl + ConServer.get('File','csvUrl')
CsvRes = os.getcwd() + ConServer.get('File','csvRes')

LogFile = ConServer.get('File', 'log') # 读取log配置

logging.basicConfig(filename=LogFile,level=logging.DEBUG,format="%(asctime)s - %(pathname)s - %(message)s",datefmt="%Y/\
%m/%d %H:%M:%S") # logging配置

# 删除旧的log
if os.path.exists(LogFile):
    os.remove(LogFile)

# 服务器配置文件url和临时保存路径
ConUrl = ConServerUrl + ConServer.get('File','conUrl')
ConRes = os.getcwd() + ConServer.get('File','conRes')

Zip_url = ConServerUrl + ConServer.get('File','zip_url') # 获取更新包url

# 获取服务器版本信息
# noinspection PyBroadException
try:
    print("\n\033[5;31;40m注意：请以管理员权限运行\033[0m\n")
    print("")
    print("\n\033[5;36;40m正在获取服务器版本信息，请稍后...\033[0m\n")
    ServerVer = requests.get(ConServerUrl + ConUrl).text

except:
    logging.debug(traceback.format_exc()) # 输出log

# 定义shell脚本路径
shellRes = ConServer.get('settings','Shell_Res')
Shell_Res = os.getcwd() + shellRes

LocalVer = ConServer.get('settings','version') # 获取本地版本
frontSpace = (50-len(LocalVer))*" " # 计算空格数量

# 打屏
print(f'''
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                     N2N_Client                     ┃
┃{frontSpace}{LocalVer}  ┃
┠────────────────────────────────────────────────────┨
┃                A Project of Nya-WSL.               ┃ 
┃ For more information,please visit: www.nya-wsl.com ┃
┃    Copyright 2021-2022. All rights reserved.       ┃
┠────────────────────────────────────────────────────┨
┃     Takahashiharuki & SHDocter      2022/11/08     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
''')

time.sleep(3.5)
os.system("clear")

try:
    time.sleep(2)
    os.system("clear")
    time.sleep(0.5)
    # noinspection PyUnboundLocalVariable
    print(f'''──────────────────────────────────────────────────────
     目前版本：{LocalVer}   最新版本：{ServerVer}
──────────────────────────────────────────────────────''') # 打印版本
    time.sleep(3)

# 版本更新
    if LocalVer != ServerVer:
        print("\n\033[5;36;40m更新中，请等待。\033[0m\n")

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

        request.urlretrieve(Zip_url,"n2n_update_linux.zip",report) # 下载更新包

# 解压更新包
#         Unzip = zipfile.ZipFile("n2n_update.zip", mode='r')
#         for names in Unzip.namelist():
#             Unzip.extract(names, os.getcwd())
#         Unzip.close()
#         time.sleep(2)

# 删除服务器配置文件并执行更新
        if os.path.exists('Ver/server.ini'):
            os.remove('Ver/server.ini')
        # os.remove('n2n_update.zip')
        os.system(Shell_Res)

except:
    logging.debug(traceback.format_exc()) # 输出log

try:
    if LocalVer == ServerVer:
        os.system("clear")
        print('''
\n\033[5;36;40m
目前已是最新版本！

正在查询可用服务器，请稍后...
\033[0m
''')
        if os.path.exists('Ver/server.ini'):
            os.remove('Ver/server.ini')
        request.urlretrieve(CsvUrl,CsvRes)
        print('查询完成！')
except:
    logging.debug(traceback.format_exc()) # 输出log

# noinspection PyBroadException
try:
    time.sleep(3)
    os.system("clear")

    Name = input('''──────────────────────────────────────────────────────
请输入组名称(分组隔离，不在同一个组将无法组网)：''')
    print('──────────────────────────────────────────────────────')

# 读取服务器列表
    with open(r'ServerList.csv',encoding='GB2312',errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        place = [row[0] for row in reader] # 服务器所在地域

    with open(r'ServerList.csv',encoding='GB2312',errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        address = [row[1] for row in reader] # 服务器IP

        os.system("clear")
        print('可用服务器列表：')
        print('──────────────────────────────────────────────────────')
        for i in place:
            print("序号：%s 服务器：%s" % (place.index(i) + 1, i))
        print('──────────────────────────────────────────────────────')
        number = int(input('请输入服务器序号，按Enter键结束：'))
        if number > len(place) or number < 1: # 判断输入值是否超出范围
            input("参数错误，请重新运行...")
            sys.exit("input error")
        Server = address[number-1]
        print (f'''
服务器地址:\033[5;36;40m{Server}\033[0m\n''')
        time.sleep(2)
        os.system("clear")

    Assign = int(input('''
──────────────────────────────────────────────────────
请选择IP分配方法

1.自动分配(推荐)
2.手动分配

──────────────────────────────────────────────────────

请输入数字并按回车确认:'''))

    time.sleep(1)
    os.system("clear")

    if Assign == 2:
        print('''
┌───────────────────────────────────────────────────┐
│                 Please wait...                    │
└───────────────────────────────────────────────────┘
''')
        address = input('请输入IP地址，并按回车确认（例：127.0.0.1）:')
        input(f'''
IP:\033[5;36;40m{address}\033[0m\n
如有误请关闭重新运行，无误请按回车确认''')
        echo = f"./edge -c {Name} -a {address} -f -l {Server}"
        os.system(echo)
    if Assign == 1:
        print('''
┌───────────────────────────────────────────────────┐
│                 Please wait...                    │
└───────────────────────────────────────────────────┘
''')
        echo = f"./edge -c {Name} -f -l {Server}"
        os.system(echo)
    else:
        input('参数错误！请重新启动程式！')
except:
    logging.debug(traceback.format_exc()) # 输出log