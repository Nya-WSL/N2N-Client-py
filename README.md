# N2N Client for NiceGUI

![python](https://img.shields.io/badge/Version-2.0.2-cyan) ![python](https://img.shields.io/badge/Python-3.11.5-blue) ![os](https://img.shields.io/badge/OS-Windows-orange) [![CircleCI](https://dl.circleci.com/status-badge/img/gh/Nya-WSL/N2N-Client-py/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/Nya-WSL/N2N-Client-py/tree/main)

### [如何使用/how to use](./How-To-Use.md)（该文档已过时）

### Build

`python build.py --name Project_Name --icon icon.ico n2n_client.py`

# 目前已知公开情报

* 我们目前并不清楚转发数据包需要占用多少资源，所以如果有大量用户同时使用的情况下，延迟可能会飙升
* 项目基于[n2n](https://github.com/ntop/n2n)以及python<s>3.9.5</s>(v1.0.2+ -> <s>3.10.4</s>> | v1.0.6+ -> 3.11.0 | v1.1.4+ -> <s>3.11.3</s> | v2.0.0+ -> 3.11.5)和TAP虚拟网卡
* 参考[n2n](https://github.com/ntop/n2n)官方说明自建服务端，实测新加坡延迟和大陆差不多（测试环境：Tabletop Simulator）
* 已知可用环境：Minecraft（java & bedrock）| Overcooked2 | Tabletop Simulator | Escape from Tarkov(Only Aki&Fika) | ······ | 理论上所有通信方式为p2p的环境都可使用（所有测试环境均未考虑服务器带宽限制以及同时使用人数，仅供参考）

# 联系我们

- [提交issues](https://github.com/Nya-WSL/issues/issues)

- [support@nya-wsl.com](mailto:support@nya-wsl.com)

- [Nya-WSL服务维护与反馈群](https://jq.qq.com/?_wv=1027&k=tSeB0sdy)

# LICENSE

- 代码授权协议采用修改过的 MIT 协议，具体内容可查看[LICENSE](LICENSE)；[N2N](https://github.com/ntop/n2n)授权协议根据软件作者采用GPLv3协议。