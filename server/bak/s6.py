#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys
import struct
import os
import time
import select

def start_server():
    # 创建 socket 对象
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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