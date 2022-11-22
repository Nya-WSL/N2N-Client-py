#!/bin/bash

sleep 2
echo 正在安装unzip...
sudo apt-get install unzip
echo 正在结束n2n进程...
pkill n2n
echo 更新中...
unzip -o n2n_update_linux.zip
rm n2n_update_linux.zip
sudo chmod -R 777 *
echo ！！！更新完成，请重新运行n2n_client！！！