#!/usr/bin/python3
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys

# 创建 socket 对象
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = socket.gethostname()
# host = '47.104.170.183'

port = 9999

# 绑定端口号
serversocket.bind((host, port))

# 设置最大连接数，超过后排队
serversocket.listen(5)

print('Server start at: %s:%s' %(host, port))
print ('wait for connection...')

while True:
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()
    print("连接地址: %s" % str(addr))
    while True:
        data = clientsocket.recv(1024)
        print(data.decode('utf-8'))
        clientsocket.send("server received you message.")
    serversocket.close()