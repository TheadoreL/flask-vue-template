#!/bin/bash

# 1. 获取当前脚本所在路径
DIR=$(cd "$(dirname "$0")" && pwd)

# 2. 创建虚拟环境
echo "Creating virtual environment..."
python -m venv .venv
source .venv/bin/activate  # Unix/macOS
#.venv\Scripts\activate  # Windows

# 3. 安装 requirements
echo "Installing requirements..."
pip install -r requirements.txt

# 4. 判断 config.ini 是否存在
if [ -f config.ini ]; then
    # 如果 config.ini 存在，读取其中的 app name
    APPNAME=$(sed -n '/^\[app\]/,/^\[/{s/^\s*name\s*=\s*\(.*\)/\1/p}' config.ini)
else
    # 如果 config.ini 不存在，从 config.ini.example 创建 config.ini
    echo "config.ini not found. Creating from config.ini.example..."
    cp config.ini.example config.ini

    # 然后尝试从 config.ini.example 读取 app name
    APPNAME=$(sed -n '/^\[app\]/,/^\[/{s/^\s*name\s*=\s*\(.*\)/\1/p}' config.ini.example)

    # 如果 config.ini.example 中没有 app name，询问用户输入
    if [ -z "$APPNAME" ]; then
        echo "No app name found in config.ini.example. Please enter an app name:"
        read APPNAME

        # 如果用户没有输入，则退出脚本
        if [ -z "$APPNAME" ]; then
            echo "App name is required. Exiting..."
            exit 1
        fi

        # 更新 config.ini.example 和 config.ini 中的 app name
        sed -i "/^\[app\]/,/^\[/{s/^\s*name\s*=.*$/name=$APPNAME/}" config.ini.example
    fi
fi

# 5. 更新 config.ini 中的 app name
sed -i "/^\[app\]/,/^\[/{s/^\s*name\s*=.*$/name=$APPNAME/}" config.ini

# 6. 复制 uwsgi 配置文件
echo "Setting up uwsgi.ini..."
cp uwsgi.ini.example uwsgi.ini

# 7. 替换 %PATH-TO-APP% 为当前路径
sed -i "s|%PATH-TO-APP%|$DIR|g" uwsgi.ini

# 8. 设置系统服务文件（适用于 Linux 或 macOS）
echo "Setting up system service..."
cp app.uwsgi.service.example "$APPNAME".uwsgi.service
sed -i "s|%PATH-TO-APP%|$DIR|g" "$APPNAME".uwsgi.service
sed -i "s|%APPNAME%|$APPNAME|g" "$APPNAME".uwsgi.service

# 9. 安装npm包
yarn

# 10. 完成设置
echo "Setup complete! You can now run your Flask app."
