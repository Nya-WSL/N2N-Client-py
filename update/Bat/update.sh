#!/bin/bash

sleep 2
echo 正在安装unzip
sudo apt-get install unzip
echo 正在结束n2n进程
pkill n2n
echo 更新中...
rm log.ini
unzip n2n_update_linux.zip
rm n2n_update_linux.zip
echo 即将重启n2n...
sleep 2
./n2n_client_linux