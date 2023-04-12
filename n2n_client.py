import os
import csv
import sys
import time
import json
import yaml
import ctypes
import datetime
import requests
from urllib import request

os.system("") # 修复win10 print颜色bug

# 检测系统类型
osInfo = sys.platform
if osInfo == "win32": # 系统类型
    clsCommand = "cls" # cmd清屏指令
    n2nEXE = "edge.exe" # windows的n2n二进制文件
    configFile = "config.local.win.yml" # windows的配置文件

elif osInfo == "linux": # 系统类型
    clsCommand = "clear" # 终端清屏指令
    n2nEXE = "./edge" # linux的n2n二进制文件
    configFile = "config.local.linux.yml"# linux的配置文件

# 读取本地配置

# c = open('config.local.win.json','r')
# text = c.read()
# c.close()
# config = json.loads(text)

with open(configFile, encoding='utf-8') as f: # 读取主配置文件
    config = yaml.load(f, Loader=yaml.FullLoader) # 转为字典

CheckServerList = config["check_server_list"]
AutoUpdate = config["auto_update"]

workDir = os.getcwd() + "\\logs"
if not os.path.exists("logs"):
    os.mkdir(workDir)
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
            level=logging.DEBUG,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
# 写入日志
        logging.debug(traceback.format_exc())

# logging.basicConfig(filename=LogFile,level=logging.DEBUG,format="%(asctime)s - %(pathname)s - %(message)s",datefmt="%Y/\
# %m/%d %H:%M:%S") # log配置

try:
    language = config["language"] #读取语言文件的字典
    if language == "auto":
        dll_h = ctypes.windll.kernel32
        SysLang = hex(dll_h.GetSystemDefaultUILanguage())
        if SysLang == "0x804":
            language = "zh_cn"
        elif SysLang == "0x409":
            language = "en_us"
        else:
            language = config["default_lang"]
    else:
        language = config["language"]
    if not os.path.exists(f"lang/{language}.json"):
        input(f"""
未发现语言文件'{language}.json'，如果确定配置没问题请重新安装程式！
The language file '{language}.json' is not found. If the configuration is right, please reinstall the program!""")
        sys.exit(f"missing language file '{language}.json' or config is error") # 带参退出并写入log
except:
    Mylogpetion()

# 读取语言配置
l = open(f'lang/{language}.json', 'r', encoding="utf-8") # 将语言文件写入缓存
LangText = l.read() # 读取语言
l.close() # 关闭语言文件
lang = json.loads(LangText) # 将语言写入字典

# 指定语言所对应的变量
StartText = lang["StartText"]
AssignTextAuto = lang["AssignTextAuto"]
AssignTextManual = lang["AssignTextManual"]
CheckVersion = lang["CheckVersion"]
LocalVersion = lang["LocalVersion"]
ServerVersion = lang["ServerVersion"]
UpdateText = lang["UpdateText"]
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
AutoUpdateText = lang["AutoUpdateText"]
AutoUpdateConfigError = lang["AutoUpdateConfigError"]
CheckServerListError = lang["CheckServerListError"]

ConServerUrl = config["server"] # 读取服务器配置

# 服务器列表获取url和临时保存路径
CsvUrl = ConServerUrl + config["Url"]["csvUrl"]
CsvRes = os.getcwd() + config["Path"]["csvRes"]
CsvFile = config["Path"]["csvFile"]

ConUrl = ConServerUrl + config["Url"]["conUrl"]# 服务器配置文件

ZipUrl = ConServerUrl + config["Url"]["zipUrl"] # 获取更新包url
UpdateUrl = ConServerUrl + config["Url"]["updateUrl"] # 获取更新模块url
UpdateRes = config["Path"]["updateRes"] # 更新模块保存路径

HistoryUrl = ConServerUrl + config["Url"]["historyUrl"] # 获取默认历史记录url
HistoryRes = config["Path"]["historyRes"] # 历史记录保存位置

# 当历史记录不存在时下载默认历史记录
if not os.path.exists("history.json"):
    request.urlretrieve(HistoryUrl,HistoryRes)

# 读取历史记录
h = open('history.json','r') # 将历史记录写入缓存
text1 = h.read() # 读取历史记录
h.close() # 关闭文件
history = json.loads(text1) # 将历史记录写入字典

HistoryServer = history["server"] # 历史服务器IP
GroupName = history["groupname"] # 历史组名称
HistoryAssign = history["dist"] # 历史IP分配方式

# 获取并定义history.json中dist的值为i18n的值
if HistoryAssign == "auto":
    AssignText = AssignTextAuto
elif HistoryAssign == "manual":
    AssignText = AssignTextManual

# 将所选择的连接方式写进history.json
def SaveHistory():
    if Assign == 1:
        AssignJson = "auto"
    if Assign == 2:
        AssignJson = "manual"
    history["server"] = Server
    history["groupname"] = Gname
    history["dist"] = AssignJson
    with open("history.json",'w',encoding='utf-8') as f:
        json.dump(history, f,ensure_ascii=False)

# 获取服务器版本信息
try:
    print(f"\n\033[5;31;40m{StartText}\033[0m\n")
    print("")
    print(f"\n\033[5;36;40m{CheckVersion}\033[0m\n")
    ServerVer = requests.get(ConUrl).text # 从资源文件服务器获取版本号
    
except:
    Mylogpetion()

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
┃    Copyright 2021-2023. All rights reserved.       ┃
┠────────────────────────────────────────────────────┨
┃               Nya-WSL      2023/04/12              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
''')

time.sleep(3.5)
os.system(clsCommand) # 清屏

try:
# 打印版本
    print(f'''──────────────────────────────────────────────────────
    {LocalVersion}：{LocalVer}   {ServerVersion}：{ServerVer}
──────────────────────────────────────────────────────''') 
    time.sleep(3)

# 版本更新
    if LocalVer != ServerVer:
        
        if AutoUpdate == True:
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

            print(f"\n\033[5;36;40m{UpdateText}\033[0m\n")

            if osInfo == "win32": # 系统类型
                request.urlretrieve(UpdateUrl,UpdateRes) # 下载更新模块
                os.system('update.exe')# 执行更新

            elif osInfo == "linux": # 系统类型
                request.urlretrieve(ZipUrl,"n2n_update_linux.zip",report) # 下载更新包
                request.urlretrieve(UpdateUrl,UpdateRes) # 下载更新脚本
                os.system("sudo chmod -R 777 *")
                os.system(UpdateRes)

        elif AutoUpdate == False:
            print(f"{AutoUpdateText}")
            time.sleep(5)
        else:
            input(f"{AutoUpdateConfigError}")
            sys.exit(f"{AutoUpdateConfigError} | error value:auto_update is {AutoUpdate}")
except:
    Mylogpetion()
    sys.exit("") # 防止python捕捉到抛出的error后继续执行程序，手动退出
    
try:
    if LocalVer == ServerVer:
        os.system(clsCommand) # 清屏
        print(f'\n\033[5;36;40m{LatestVersion}\033[0m')
        hist = input(f"{HistoryChoose}{HistoryServer}{HistoryChoose1}{GroupName}{HistoryChoose2}{AssignText}{HistoryChoose3}") # 确认读取历史记录的echo
        if hist == "" or hist ==  "y" or hist == "Y": # 上方hist的值为:空/y/Y
            os.system(clsCommand) # 清屏
            Assign = HistoryAssign # 定义分配方式为历史记录
            if Assign == "manual": # 判断分配方式是否为手动
                address = input(lang["IP"]) # 手动输入IP段
                input(f'''
IP:\033[5;36;40m{address}\033[0m\n
{SecondCheck}''') # 二次确认
                if osInfo == "win32":
                    n2nManual = f"{n2nEXE} -c {GroupName} -a {address} -l {HistoryServer}" # 定义n2n的参数
                    n2nAuto = f"{n2nEXE} -c {GroupName} -l {HistoryServer}"
                elif osInfo == "linux":
                    n2nManual = f"{n2nEXE} -c {GroupName} -a {address} -f -l {HistoryServer}" # 定义n2n的参数
                    n2nAuto = f"{n2nEXE} -c {GroupName} -f -l {HistoryServer}"
                os.system(n2nManual)# 运行n2n的边缘节点并跟参
            if Assign == "auto": # 判断分配方式是否为自动
                if osInfo == "win32":
                    n2nAuto = f"{n2nEXE} -c {GroupName} -l {HistoryServer}"
                elif osInfo == "linux":
                    n2nAuto = f"{n2nEXE} -c {GroupName} -f -l {HistoryServer}"
                os.system(n2nAuto)# 运行n2n的边缘节点并跟参
            # 如果历史记录里的分配方式为错误的值将按照自动分配的方式运行
            else:
                print(lang["AssignError"]) # 输出error
                time.sleep(2)
                if osInfo == "win32":
                    n2nAuto = f"{n2nEXE} -c {GroupName} -l {HistoryServer}"
                elif osInfo == "linux":
                    n2nAuto = f"{n2nEXE} -c {GroupName} -f -l {HistoryServer}"
                os.system(n2nAuto)# 运行n2n的边缘节点并跟参
            
        elif hist == "n" or hist == "N": # 上方hist的值为:n/N
            print(f'\n\033[5;36;40m{SearchServer}\033[0m') # 输出echo
            request.urlretrieve(CsvUrl,CsvRes) # 下载可用服务器列表
            if CheckServerList == "offline":
                LocalList = config["Path"]["local_list"]
                if not os.path.exists(LocalList):
                    LocalList = CsvFile
                    print(f"{CheckServerListError}")
                    time.sleep(5)
            if CheckServerList == "online":
                LocalList = CsvFile
            print(lang["SearchSuccess"]) # 输出echo
            time.sleep(3)
            os.system(clsCommand) # 清屏

            # 提示用户手动输入组名称
            Gname = input(f'''──────────────────────────────────────────────────────
{InputGroupName}''')
            print('──────────────────────────────────────────────────────')

            # 读取服务器列表
            
            with open(rf'{LocalList}',encoding='GB2312',errors='ignore') as csvfile:
                reader = csv.reader(csvfile)
                place = [row[0] for row in reader] # 服务器所在地域

            with open(rf'{LocalList}',encoding='GB2312',errors='ignore') as csvfile:
                reader = csv.reader(csvfile)
                address = [row[1] for row in reader] # 服务器IP

                os.system(clsCommand) # 清屏
                print(lang["ServerList"])
                print('──────────────────────────────────────────────────────')
                for i in place:
                    print(f"{ServerNumber}%s {ServerName}%s" % (place.index(i) + 1, i))# 根据csv文件所写的地域输出格式化列表
                print('──────────────────────────────────────────────────────')
                number = int(input(lang["ServerText"])) # 用户所选择的服务器
                if number > len(place) or number < 1: # 判断输入值是否超出范围
                    # 抛出错误写入log并退出
                    input(lang["ParameterError"])
                    sys.exit("input error")
                # 将用户所选择的服务器序号和csv中的服务器IP对应
                Server = address[number-1]
                print (f'''
{ServerIP}\033[5;36;40m{Server}\033[0m\n''')
                time.sleep(2)
                os.system(clsCommand)
            # 输出分配方式让用户手动选择
            Assign = int(input(f'''
──────────────────────────────────────────────────────
{AssignText}

1.{AssignTextAuto}
2.{AssignTextManual}

──────────────────────────────────────────────────────

{ConfirmText}'''))

            time.sleep(1)
            os.system(clsCommand)

            if Assign == 2: # 手动分配
                SaveHistory()
                address = input(lang["IP"])
                input(f'''
IP:\033[5;36;40m{address}\033[0m\n
{SecondCheck}''')
                if osInfo == "win32":
                    n2nManual = f"{n2nEXE} -c {Gname} -a {address} -l {Server}" # 定义n2n的参数
                    n2nAuto = f"{n2nEXE} -c {Gname} -l {Server}"
                elif osInfo == "linux":
                    n2nManual = f"{n2nEXE} -c {Gname} -a {address} -f -l {Server}" # 定义n2n的参数
                    n2nAuto = f"{n2nEXE} -c {Gname} -f -l {Server}"
                os.system(n2nManual)
            if Assign == 1: # 自动分配
                SaveHistory()
                if osInfo == "win32":
                    n2nAuto = f"{n2nEXE} -c {Gname} -l {Server}"
                elif osInfo == "linux":
                    n2nAuto = f"{n2nEXE} -c {Gname} -f -l {Server}"
                os.system(n2nAuto)
            else:
                input(lang["ParameterError"])
        else: # 上方hist的值出现错误
            input(lang["ParameterError"])
            sys.exit("history choose is error") # 抛出错误写入log并退出
            
except:
    Mylogpetion()