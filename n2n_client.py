import os
import sys
import random

os.system('')

name = input('请输入组名称(分组隔离，如不在同一个组将无法组网)：')

a = int(input('''
┌─────────────────────────────────────────────┐
│                  n2n_client          v0.0.3 │ 
├─────────────────────────────────────────────┤
│请选择IP分配方法                             │
│1.手动分配                                   │
│2.自动分配(推荐)                             │
├─────────────────────────────────────────────┤
│   Takahashiharuki SHDocter       2021/12/24 │
├─────────────────────────────────────────────┤
│                圣诞节快乐~~~                │
└─────────────────────────────────────────────┘
请输入数字并按回车确认:
'''))
print('''
┌─────────────────────────────────────────────┐
│             Please waiting...               │
└─────────────────────────────────────────────┘
''')

if a == 1:
    ip = int(input('请输入IP地址最后一组的数字，并按回车确认（例：71.94.86.13 只需要输入13）:'))
    address = '71.94.86.%d'%ip
    input(f'IP:{address} 如有误请关闭重新运行，无误请按回车确认')
    echo = f"edge.exe -c {name} -a {address} -l n2n.osttsstudio.ltd:7777"
    os.system(echo)
if a == 2:
    # add4 = (random.sample(range(1,255),1)).pop()
    # address = '71.94.86.%d'%add4
    # input(f'IP:{address} 如有误请关闭重新运行，无误请按回车确认')
    echo = f"edge.exe -c {name} -l n2n.osttsstudio.ltd:7777"
    os.system(echo)
elif a != 1 and 2:
    input('参数错误！请关闭本窗口后重新启动！')