# 如何使用

### 因为修改网卡需要管理员账号，请先将n2n-client.exe和edge.exe任意一个设置为用管理员权限运行（自行百度）

### 1、安装TAP虚拟网卡（默认设置）

  ![1](D:\GitHub\N2N-Client-py\img\1.png)

### 2、运行n2n_client.exe

### 3、输入组名称

  ![2](D:\GitHub\N2N-Client-py\img\2.png)
  ![3](D:\GitHub\N2N-Client-py\img\3.png)

### 4、选择IP分配方式

  ![4](D:\GitHub\N2N-Client-py\img\4.png)

* 手动分配：手动自定义IP（暂时不支持自定义IP段，所以每个分组理论上限255名用户），例：IP为192.168.100.13，只需要输入最后一段的13，前面三段目前版本无法自定义。

* 自动分配：从服务端获取IP（v0.0.3+）。

### 5、确认信息

![5](D:\GitHub\N2N-Client-py\img\5.png)
![6](D:\GitHub\N2N-Client-py\img\6.png)

### 6、二次确认

<font color=red size=5px>请确认组名和IP，如果不在同一个组将无法联机</font>
![7](D:\GitHub\N2N-Client-py\img\7.png)

参数解释：-c 组名 -a 分配给你的内网IP -l 服务器IP

（因为return比较麻烦，最近几个版本没有写return的打算，如果输入错误只能关闭程序重新启动，未来版本可能会写）

### 7、成功启动

 ![10](D:\GitHub\N2N-Client-py\img\10.png)