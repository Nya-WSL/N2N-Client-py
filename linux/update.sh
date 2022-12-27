#!/bin/bash

screen=$"n2n"

color() {
	Green="\033[32m"
	Red="\033[31m"
	Yellow="\033[33m"
	RedBG="\033[41;37m"
	Font="\033[0m"
}

info() {
	echo "[*] $*"
}

error() {
	echo -e "${Red}[-]${Font} $*"
	exit 1
}

success() {
	echo -e "${Green}[+]${Font} $*"
}

warning() {
	echo -e "${Yellow}[*]${Font} $*"
}

panic() {
	echo -e "${RedBG}$*${Font}"
	exit 1
}

version() {
    source /etc/os-release || source /usr/lib/os-release || panic "不支持此操作系统"
    if [[ $ID == "centos" ]]; then
	    PM="yum"
	    INS="sudo yum install -y -q"
    elif [[ $ID == "debian" || $ID == "ubuntu" ]]; then
	    PM="apt-get"
	    INS="sudo apt-get install -y -q"
    else
	    error "不支持此操作系统"
    fi
}


install() {
    info "正在安装软件包"
    rpm_packages="unzip openssl"
    apt_packages="unzip openssl"
    if [[ $PM == "apt-get" ]]; then
	    $PM update
	    $INS $apt_packages
    elif [[ $PM == "yum" || $PM == "dnf" ]]; then
	    sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
        $PM update
	    $INS $rpm_packages
    fi
    success "软件包安装成功"
}

update() {
    sleep 2
    info "正在结束n2n进程..."
    pkill n2n
    info "更新中..."
    unzip -o n2n_update_linux.zip
    rm n2n_update_linux.zip
    sudo chmod -R 777 *
    success "更新完成，即将重新运行n2n_client"
    sleep 2
    ./n2n_client_linux
}

main() {
    color
    version
    install
    update
}

main "$*"