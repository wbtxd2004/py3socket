#!/usr/bin/python3
# 文件名：client.py

# 导入 socket、sys 模块
import socket
import sys

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
# host = socket.gethostname()
host = '47.104.170.183'

# 设置端口号
port = 9999

# 连接服务，指定主机和端口
s.connect((host, port))

while True:
    cmd = input("Please input msg:")
    s.send(cmd.encode('utf-8'))
    data = s.recv(1024)
    print(data)
s.close
