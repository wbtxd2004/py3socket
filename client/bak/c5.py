#!/usr/bin/python3
# 文件名：client.py

# 导入 socket、sys 模块
import socket
import sys
import time

# 创建 socket 对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
# host = socket.gethostname()
host = '47.104.170.183'

# 设置端口号
port = 9999

# 连接服务，指定主机和端口
client.connect((host, port))
while True:
    data = client.recv(1024)
    print("the data received is:",data)
    client.send(b"hihi I am client")
    client.close()