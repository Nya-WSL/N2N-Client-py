import os
import logging
import traceback
import csv
from urllib import request

if os.path.exists('debug.log'):
    os.remove('debug.log') # del old log file

logging.basicConfig(filename='debug.log',level=logging.DEBUG,format="%(asctime)s - %(pathname)s - %(message)s",datefmt=\
"%Y/%m/%d %H:%M:%S")
CsvUrl = "http://qn.osttsstudio.ltd/files/ServerList.csv"
CsvRes = os.getcwd() + "./ServerList.csv"

try:
    request.urlretrieve(CsvUrl,CsvRes)
except:
    logging.debug(traceback.format_exc())

os.system('')

print('''
┌───────────────────────────────────────────────────┐
│              n2n_client      v1.0.1               │ 
├───────────────────────────────────────────────────┤
│       Project Nya-WSL.  All rights reserved.      │ 
│ For more information,please visit:www.nya-wsl.com │
├───────────────────────────────────────────────────┤
│     Takahashiharuki&SHDocter       2022/03/15     │
└───────────────────────────────────────────────────┘
''')

try:
    Name = input('请输入组名称(分组隔离，不在同一个组将无法组网)：')
    print('-------------------------------------------')
    with open(r'./ServerList.csv',encoding='GB2312',errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        place = [row[0] for row in reader]

    with open(r'./ServerList.csv',encoding='GB2312',errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        address = [row[1] for row in reader]

        print('可用服务器列表：')
        print('-------------------------------------------')
        for i in place:
            print("序号：%s 服务器：%s" % (place.index(i) + 1, i))
        print('-------------------------------------------')
        number = int(input('请输入服务器序号，按Enter键结束：'))
        Server = address[number-1]
        print (f'服务器地址:{Server}')
        
    # ConServer = ConfigParser()
    # ConServer.read('n2n.ini')

    # Server = ConServer.get('setting','Server') + ".n2n.osttsstudio.ltd"

# 中国北京:bj.n2n.osttsstudio.ltd:7777
# 中国上海:sh.n2n.osttsstudio.ltd:7777
# 中国香港:hk.n2n.osttsstudio.ltd:7777

    Assign = int(input('''
-------------------------------------------
请选择IP分配方法
1.手动分配
2.自动分配(推荐)


-------------------------------------------
请输入数字并按回车确认:'''))
    print('''
┌───────────────────────────────────────────────────┐
│                 Please wait...                    │
└───────────────────────────────────────────────────┘
''')

    # if Server == 1:
    #     IP = "n2n.osttsstudio.ltd:7777"
    # if Server == 2:
    #     IP = "n2n.haruki.top:7777"
    # elif Server != 1 and 2:
    #     input('参数错误！请关闭本窗口后重新启动！')

    if Assign == 1:
        ip = int(input('请输入IP地址最后一组的数字，并按回车确认（例：71.94.86.13 只需要输入13）:'))
        address = '71.94.86.%d'%ip
        input(f'IP:{address} 如有误请关闭重新运行，无误请按回车确认')
        echo = f"edge.exe -c {Name} -a {address} -l {Server}"
        os.system(echo)
    if Assign == 2:
    # add4 = (random.sample(range(1,255),1)).pop()
    # address = '71.94.86.%d'%add4
    # input(f'IP:{address} 如有误请关闭重新运行，无误请按回车确认')
        echo = f"edge.exe -c {Name} -l {Server}"
        os.system(echo)
    elif Assign != 1 and 2:
        input('参数错误！请关闭本窗口后重新启动！')
except:
    logging.debug(traceback.format_exc())