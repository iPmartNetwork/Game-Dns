#!/bin/bash

echo "شروع نصب پنل مدیریت DNS گیمینگ..."

if [ "$EUID" -ne 0 ]
then 
  echo "لطفا با دسترسی root اجرا کنید!"
  exit
fi

echo "آپدیت پکیج‌ها..."
apt update -y
apt upgrade -y

if ! command -v docker &> /dev/null
then
    echo "Docker پیدا نشد. درحال نصب Docker..."
    apt install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    apt update
    apt install -y docker-ce
    systemctl start docker
    systemctl enable docker
else
    echo "Docker قبلا نصب شده است."
fi

if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose پیدا نشد. درحال نصب Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "Docker Compose قبلا نصب شده است."
fi

echo "اکسترکت پروژه و اجرای سرویس‌ها..."
docker-compose up --build -d

echo "✅ نصب کامل شد!"
echo "🌐 آدرس پروژه: http://SERVER-IP:5000"
echo "ریپازیتوری: https://github.com/iPmartNetwork/Game-Dns"