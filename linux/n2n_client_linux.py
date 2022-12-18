import os
import csv
import sys
import time
import json
import logging
import requests
import traceback
from urllib import request

# 读取本地配置
c = open('config.local.linux.json','r')
text = c.read()
c.close()
config = json.loads(text)

# 读取历史记录
h = open('history.json',"r")
text1 = h.read()
h.close()
history = json.loads(text1)

HistoryServer = history["server"]
GroupName = history["groupname"]
HistoryAssign = history["dist"]

if HistoryAssign == "auto":
    AssingText = "自动分配"
elif HistoryAssign == "manual":
    AssingText = "手动分配"

def SaveHistory():
    history["server"] = Server
    history["groupname"] = Name
    if Assign == 1:
        AssignJson = "auto"
    if Assign == 2:
        AssignJson = "manual"
    history["dist"] = AssignJson
    with open("history.json",'w',encoding='utf-8') as f:
        json.dump(history, f,ensure_ascii=False)

ConServerUrl = config["server"] # 读取服务器配置

# 服务器列表获取url和临时保存路径
CsvUrl = ConServerUrl + config['Path']['csvUrl']
CsvRes = os.getcwd() + config['Path']['csvRes']

LogFile = config['Path']['log'] # 读取log配置

# 删除旧的log
if os.path.exists(LogFile):
    os.remove(LogFile)

logging.basicConfig(filename=LogFile,level=logging.DEBUG,format="%(asctime)s - %(pathname)s - %(message)s",datefmt="%Y/\
%m/%d %H:%M:%S") # log配置

ConUrl = ConServerUrl + config['Path']['conUrl']# 服务器配置文件

ZipUrl = ConServerUrl + config['Path']['zipUrl'] # 获取更新包url
UpdateUrl = ConServerUrl + config['Path']['updateUrl'] # 获取更新程序url
UpdateRes = config['Path']['updateRes']

# 获取服务器版本信息
# noinspection PyBroadException
try:
    print("\n\033[5;31;40m注意：请以管理员权限运行\033[0m\n")
    print("")
    print("\n\033[5;36;40m正在获取服务器版本信息，请稍后...\033[0m\n")
    ServerVer = requests.get(ConUrl).text.strip()
    
except:
    logging.debug(traceback.format_exc()) # 输出log

# 定义shell脚本路径
shellRes = config['Path']['shellRes']
Shell = os.getcwd() + shellRes

LocalVer = config['version'] # 获取本地版本
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
┃     Takahashiharuki & SHDocter      2022/12/11     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
''')

time.sleep(3.5)
os.system("clear")

try:
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

        request.urlretrieve(ZipUrl,"n2n_update_linux.zip",report) # 下载更新包
        request.urlretrieve(UpdateUrl,UpdateRes) # 下载更新脚本
        os.system("sudo chmod -R 777 *")
        os.system(Shell)

except:
    logging.debug(traceback.format_exc()) # 输出log
    sys.exit("update error")
    
try:
    if LocalVer == ServerVer:
        os.system("clear")
        print('\n\033[5;36;40m目前已是最新版本！\033[0m')
        hist = input(f"是否继续连接{HistoryServer}和组{GroupName}和{AssingText}IP？默认:y(y/N)")
        if hist == None or "y" or "Y":
            os.system("clear")
            Assign = HistoryAssign
            if Assign == "manual":
                address = input('请输入IP地址，并按回车确认（例：127.0.0.1）:')
                input(f'''
IP:\033[5;36;40m{address}\033[0m\n
如有误请关闭重新运行，无误请按回车确认''')
                echo = f"./edge -c {GroupName} -a {address} -f -l {HistoryServer}"
                os.system(echo)
            if Assign == "auto":
                echo = f"./edge -c {GroupName} -f -l {HistoryServer}"
                os.system(echo)
            else:
                input(f'参数错误！错误参数为：{Assign},请确保“history.json”中的“dist”参数为“auto”或者“manual”然后重启程式！')
            
        elif hist == "n" or "N":
            print('\n\033[5;36;40m正在查询可用服务器，请稍后...\033[0m')
            request.urlretrieve(CsvUrl,CsvRes)
            print('查询完成！')
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
                SaveHistory()
                os.system(echo)
            if Assign == 1:
                print('''
┌───────────────────────────────────────────────────┐
│                 Please wait...                    │
└───────────────────────────────────────────────────┘
''')
                echo = f"./edge -c {Name} -f -l {Server}"
                SaveHistory()
                os.system(echo)
            else:
                input('参数错误！请重新启动程式！')
        else:
            input("参数错误！请重新启动程式！")
            sys.exit("history choose is error")
            
except:
    logging.debug(traceback.format_exc()) # 输出log