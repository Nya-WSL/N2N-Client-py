

![python](https://img.shields.io/badge/Python-3.10-blue)![os](https://img.shields.io/badge/OS-Windows-orange)[![CircleCI](https://dl.circleci.com/status-badge/img/gh/Nya-WSL/N2N-Client-py/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/Nya-WSL/N2N-Client-py/tree/main)[![Codacy Badge](https://app.codacy.com/project/badge/Grade/2c57ea2ee77f4860a02479f27d76def0)](https://www.codacy.com/gh/Nya-WSL/N2N-Client-py/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Nya-WSL/N2N-Client-py&amp;utm_campaign=Badge_Grade)

# 如何使用

### 因为修改网卡需要管理员账号，请先将n2n-client.exe和edge.exe任意一个设置为用管理员权限运行（自行百度）

### 1、安装TAP虚拟网卡（默认设置）
  ![1](img/1.png)

### 2、运行n2n_client.exe

### 3、输入组名称
  ![2](img/2.png)
  ![3](img/3.png)

### 4、选择IP分配方式
  ![4](img/4.png)

* 手动分配：手动自定义IP（暂时不支持自定义IP段，所以每个分组理论上限255名用户），例：IP为192.168.100.13，只需要输入最后一段的13，前面三段目前版本无法自定义。

* 自动分配：从服务端获取IP（v0.0.3+）。

### 5、确认信息

![5](img/5.png)
![6](img/6.png)

### 6、二次确认

<font color=red size=5px>请确认组名和IP，如果不在同一个组将无法联机</font>
![7](img/7.png)

参数解释：-c 组名 -a 分配给你的内网IP -l 服务器IP

（因为return比较麻烦，最近几个版本没有写return的打算，如果输入错误只能关闭程序重新启动，未来版本可能会写）

### 7、成功启动

 ![10](img/10.png)

# 目前已知公开情报

* 我们目前并不清楚转发数据包需要占用多少资源，所以如果有大量用户同时使用的情况下，延迟可能会飙升
* 本项目来源于EasyN2N
* 本项目目前只是早期版本，会在未来逐渐完善，也欢迎有大佬加入本项目一起敲代码
* 项目基于[n2n](https://github.com/ntop/n2n)以及python<s>3.9.5</s>(v1.0.2+ -> 3.10.4)和TAP虚拟网卡
* 因为是公益项目，这种项目应该也不会有人会接手，所以在可以预见的未来，本项目会停止维护，我们不接受任何资金方面的帮助，欢迎有人一起来维护本项目（[GitHub](https://github.com/osttsStudio/N2N-Client-py)）
* 因为是早期版本，所以目前节点较少（todo：ubuntu一键安装脚本&取消公益服务器），实测新加坡延迟和大陆差不多（测试环境：Tabletop Simulator）
* N2N原理：在NAT环境较好的情况下点对点打洞，也就是所谓的p2p，在NAT环境较复杂或者根本无法打洞的情况下通过服务器中转数据包，如有需求，未来版本也可以设置强制服务器中转，因为并不推荐该方法，所以这方面的更新优先度较低，可以运行edge.exe自行跟参
### 基于上方的原理，客户端之间的延迟算法为：
* p2p：host1到host2的延迟
* 中转：host1到服务器的延迟 + host2到服务器的延迟
# 写在最后的废话

我们并不知道这个项目会不会像以前的许多项目一样因为各种各样的原因半路夭折，比如来自现实和工作的压力，比如自身能力的不足，但至少在现在的时间点，我们还保持着热血，还能趁着年少，去做自己喜爱的事情。

<center>狐日泽&高橋はるき</center>

<center>SHDocter&TakahashiHaruki</center>
