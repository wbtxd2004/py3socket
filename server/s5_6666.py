#!/usr/bin/python3
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys
import struct
import os
import time

# 创建 socket 对象
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = socket.gethostname()
# host = '47.104.170.183'

port = 6666

# 绑定端口号
serversocket.bind((host, port))

# 设置最大连接数，超过后排队
serversocket.listen(5)

print('Server start at: %s:%s' %(host, port))
print ('wait for connection...')

while True:
    # 建立客户端连接
    cs, addr = serversocket.accept()
    # print("get connected from:", addr)
    cs.send(b"begin")
    ra = cs.recv(1024)
    cs.send(ra)
    cs.send(b"over")
    # print(ra)
    cs.close()
    now_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    file_path = '/opt/socket/'+now_time+'.txt'
    f = open(file_path , 'wb')
    f.write(ra)
    f.close()
    # print('save in', file_path)