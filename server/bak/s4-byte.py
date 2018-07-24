#!/usr/bin/python3
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys
import struct
import os
import binascii
from time import ctime
if __name__ == "__main__":
    # 创建 socket 对象
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = socket.gethostname()
    # host = '47.104.170.183'
    port = 9999
    # 绑定端口号
    server.bind((host, port))
    # 设置最大连接数，超过后排队
    server.listen(5)
    print('Server start at: %s:%s' %(host, port))
    print ('wait for connection...')
    while True:
        tcpCliSock, addr = server.accept()
        print('...connected from:', addr)
        while True:
            data = tcpCliSock.recv(1024)
            data = str(binascii.b2a_hex(data))[2:-1]
            data=data.upper()
            print(data)
            # print(type(data))
            # print(data.encode('hex'))
            if not data:
                break
            # tcpCliSock.send('[%s] %s' % (ctime(), data))
            # tcpCliSock.close()　　　　　　　　#如果接收完，就断开的话，下次再发送就会报错，书本上有问题
    tcpSerSocket.close()
