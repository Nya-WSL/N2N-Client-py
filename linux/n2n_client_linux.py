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

LogFile = config["Path"]["log"] # 读取log配置

# 删除旧的log
if os.path.exists(LogFile):
    os.remove(LogFile)

logging.basicConfig(filename=LogFile,level=logging.DEBUG,format="%(asctime)s - %(pathname)s - %(message)s",datefmt="%Y/\
%m/%d %H:%M:%S") # log配置

try:
    language = config["language"]
    if not os.path.exists(f"lang/{language}.json"):
        print(f"未发现语言文件'{language}.json'，如果确定配置没问题请重新安装程式！")
        input(f"The language file '{language}.json' is not found. If the configuration is right, please reinstall the program!")
        sys.exit(f"missing language file '{language}.json' or config is error")
except:
    logging.debug(traceback.format_exc()) # 输出log

# 读取语言配置
l = open(f'lang/{language}.json', 'r', encoding="utf-8")
LangText = l.read()
l.close()
lang = json.loads(LangText)

# 读取语言
StartText = lang["StartText"]
AssingTextAuto = lang["AssingTextAuto"]
AssingTextManual = lang["AssingTextManual"]
CheckVersion = lang["CheckVersion"]
LocalVersion = lang["LocalVersion"]
ServerVersion = lang["ServerVersion"]
UpdataText = lang["UpdataText"]
LatestVersion = lang["LatestVersion"]
HistoryChoose = lang["HistoryChoose"]
HistoryChoose1 = lang["HistoryChoose1"]
HistoryChoose2 = lang["HistoryChoose2"]
HistoryChoose3 = lang["HistoryChoose3"]
SecondCheck = lang["SecondCheck"]
SearchServer = lang["SearchServer"]
InputGroupName = lang["InputGroupName"]
ServerNumber = lang["ServerNumber"]
ServerName = lang["ServerName"]
ServerIP = lang["ServerIP"]
AssignText = lang["AssignText"]
ConfirmText = lang["ConfirmText"]

# 读取服务器配置
ConServerUrl = config["resource_server"] 
UpdateServerUrl = config["update_server"]

# 服务器列表获取url和临时保存路径
CsvUrl = ConServerUrl + config["Path"]["csvUrl"]
CsvRes = os.getcwd() + config["Path"]["csvRes"]

ConUrl = UpdateServerUrl + config["Path"]["conUrl"]# 服务器配置文件

ZipUrl = UpdateServerUrl + config["Path"]["zipUrl"] # 获取更新包url
UpdateUrl = ConServerUrl + config["Path"]["updateUrl"] # 获取更新程序url
UpdateRes = config["Path"]["updateRes"]

HistoryUrl = ConServerUrl + config["Path"]["historyUrl"]
HistoryRes = config["Path"]["historyRes"]

if not os.path.exists("history.json"):
    request.urlretrieve(HistoryUrl,HistoryRes)

# 读取历史记录
h = open('history.json','r')
text1 = h.read()
h.close()
history = json.loads(text1)

HistoryServer = history["server"]
GroupName = history["groupname"]
HistoryAssign = history["dist"]

if HistoryAssign == "auto":
    AssingText = AssingTextAuto
elif HistoryAssign == "manual":
    AssingText = AssingTextManual

def SaveHistory():
    if Assign == 1:
        AssignJson = "auto"
    if Assign == 2:
        AssignJson = "manual"
    history["server"] = Server
    history["groupname"] = Name
    history["dist"] = AssignJson
    with open("history.json",'w',encoding='utf-8') as f:
        json.dump(history, f,ensure_ascii=False)

# 获取服务器版本信息
# noinspection PyBroadException
try:
    print(f"\n\033[5;31;40m{StartText}\033[0m\n")
    print("")
    print(f"\n\033[5;36;40m{CheckVersion}\033[0m\n")
    ServerVer = requests.get(ConUrl).text
    
except:
    logging.debug(traceback.format_exc()) # 输出log

# 定义shell脚本路径
shellRes = config['Path']['shellRes']
Shell = os.getcwd() + shellRes

LocalVer = config["version"] # 获取本地版本
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
┃     Takahashiharuki & SHDocter      2022/12/20     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
''')

time.sleep(3.5)
os.system("clear")

try:
    # noinspection PyUnboundLocalVariable
    print(f'''──────────────────────────────────────────────────────
    {LocalVersion}：{LocalVer}   {ServerVersion}：{ServerVer}
──────────────────────────────────────────────────────''') # 打印版本
    time.sleep(3)

# 版本更新
    if LocalVer != ServerVer:
        print(f"\n\033[5;36;40m{UpdataText}\033[0m\n")

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
        print(f'\n\033[5;36;40m{LatestVersion}\033[0m')
        hist = input(f"{HistoryChoose} + {HistoryServer} + {HistoryChoose1} + {GroupName} + {HistoryChoose2} + {AssingText} + {HistoryChoose3}")
        if hist == "" or hist ==  "y" or hist == "Y":
            os.system("clear")
            Assign = HistoryAssign
            if Assign == "manual":
                address = input(lang["IP"])
                input(f'''
IP:\033[5;36;40m{address}\033[0m\n
{SecondCheck}''')
                echo = f"./edge -c {GroupName} -a {address} -f -l {HistoryServer}"
                os.system(echo)
            if Assign == "auto":
                echo = f"./edge -c {GroupName} -f -l {HistoryServer}"
                os.system(echo)
            else:
                print(lang["AssignError"])
                time.sleep(2)
                echo = f"./edge -c {GroupName} -f -l {HistoryServer}"
                os.system(echo)
            
        elif hist == "n" or hist == "N":
            print(f'\n\033[5;36;40m{SearchServer}\033[0m')
            request.urlretrieve(CsvUrl,CsvRes)
            print(lang["SearchSuccess"])
            time.sleep(3)
            os.system("clear")

            Name = input(f'''──────────────────────────────────────────────────────
{InputGroupName}''')
            print('──────────────────────────────────────────────────────')

            # 读取服务器列表
            with open(r'ServerList.csv',encoding='GB2312',errors='ignore') as csvfile:
                reader = csv.reader(csvfile)
                place = [row[0] for row in reader] # 服务器所在地域

            with open(r'ServerList.csv',encoding='GB2312',errors='ignore') as csvfile:
                reader = csv.reader(csvfile)
                address = [row[1] for row in reader] # 服务器IP

                os.system("clear")
                print(lang["ServerList"])
                print('──────────────────────────────────────────────────────')
                for i in place:
                    print(f"{ServerNumber}%s {ServerName}%s" % (place.index(i) + 1, i))
                    print('──────────────────────────────────────────────────────')
                    number = int(input(lang["ServerText"]))
                if number > len(place) or number < 1: # 判断输入值是否超出范围
                    input(lang["ParameterError"])
                    sys.exit("input error")
                Server = address[number-1]
                print (f'''
{ServerIP}\033[5;36;40m{Server}\033[0m\n''')
                time.sleep(2)
                os.system("clear")

            Assign = int(input(f'''
──────────────────────────────────────────────────────
{AssignText}

1.{AssingTextAuto}
2.{AssingTextManual}

──────────────────────────────────────────────────────

{ConfirmText}'''))

            time.sleep(1)
            os.system("clear")

            if Assign == 2:
                address = input(lang["IP"])
                input(f'''
IP:\033[5;36;40m{address}\033[0m\n
{SecondCheck}''')
                echo = f"./edge -c {Name} -f -a {address} -l {Server}"
                SaveHistory()
                os.system(echo)
            if Assign == 1:
                echo = f"./edge -c {Name} -f -l {Server}"
                SaveHistory()
                os.system(echo)
            else:
                input(lang["ParameterError"])
        else:
            input(lang["ParameterError"])
            sys.exit("history choose is error")
            
except:
    logging.debug(traceback.format_exc()) # 输出log