

![python](https://img.shields.io/badge/Version-1.1.0-cyan) ![python](https://img.shields.io/badge/Python-3.11.0-blue) ![os](https://img.shields.io/badge/OS-Windows-orange) [![CircleCI](https://dl.circleci.com/status-badge/img/gh/Nya-WSL/N2N-Client-py/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/Nya-WSL/N2N-Client-py/tree/main)

### Linux版请使用root账户运行，目前暂不清楚使用拥有root权限的其他账号运行是否会有bug

### [如何使用/how to use](./How-To-Use.md)（该文档已过时，仅供参考，新的文档正在编写中）

### [All Release & Update Source](https://github.com/Nya-WSL/N2N-Client-Release)

# 目前已知公开情报

* 我们目前并不清楚转发数据包需要占用多少资源，所以如果有大量用户同时使用的情况下，延迟可能会飙升
* 本项目来源于EasyN2N
* 项目基于[n2n](https://github.com/ntop/n2n)以及python<s>3.9.5</s>(v1.0.2+ -> <s>3.10.4</s>> | v1.0.6+ -> 3.11.0)和TAP虚拟网卡
* 因为是公益项目，所以在可以预见的未来，本项目会停止维护，我们不接受任何资金方面的帮助，欢迎有人一起来维护本项目（[GitHub](https://github.com/Nya-WSL/N2N-Client-py)）
* 因为成本原因，目前节点较少，推荐参考[n2n](https://github.com/ntop/n2n)官方说明自建服务端（todo：取消公益服务器），实测新加坡延迟和大陆差不多（测试环境：Tabletop Simulator）
* N2N原理：在NAT环境较好的情况下点对点打洞，也就是所谓的p2p，在NAT环境较复杂或者根本无法打洞的情况下通过服务器中转数据包，也可以设置强制服务器中转，如有这方面需求请运行edge.exe自行跟参
### 基于上方的原理，客户端之间的延迟算法为：
* p2p：host1到host2的延迟
* 中转：host1到服务器的延迟 + host2到服务器的延迟

# 联系我们

- 提交issues

- 抄送邮件：support@nya-wsl.com

