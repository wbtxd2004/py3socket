#!/usr/bin/python3
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys
import struct
import os
import time
import binascii

import os

try:
    # 创建 socket 对象
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = socket.gethostname()
    # host = '127.0.0.1'
    port = 9999
    # 绑定端口号
    serversocket.bind((host, port))
    # 设置最大连接数，超过后排队
    serversocket.listen(5)
    print('Server start at: %s:%s' %(host, port))
    while True:
        print('wait for connection...')
        # 建立客户端连接
        cs, addr = serversocket.accept()
        # print("get connected from:", addr)
        print('...connected from:', addr)
        count = 0
        while True:
            # cs.send(b"begin")
            ra = cs.recv(1024)
            # cs.send(ra)
            # cs.send(b"over")
            # print(ra)
            if not ra:
                print("no data")
                break
            else:
                # print(ra)
                str1 = b''
                str2 = ''
                str3 = ''
                str_back = ''
                len_re =''
                while ra:
                    str1 = ra[0:1]
                    x = struct.unpack('B', str1)
                    y = hex(x[0])[2:]
                    if len(y) == 1:
                        str2 += '0'+y+' '
                        if count < 15:
                            str_back +=  '0'+y+' '
                    else:
                        str2 += y+' '
                        if count < 15:
                            str_back +=  y+' '
                    str3 += hex(x[0])
                    ra = ra[1:]
                    if count == 11:
                        len_re = y
                    elif count == 12:
                        len_re = y+len_re
                    count = count+1
                cs.send(bytes(str_back, 'utf-8'))
                data_len = len(str2.replace(' ',''))/2 - 15
                re_len = int(len_re,16)
                if data_len != re_len:
                    print('data not match')
                    # cs.send(bytes(re_len, 'utf-8'))
                    break
                else:
                    # print(data_len)
                    # print(re_len)
                    now_date = time.strftime("%Y%m%d", time.localtime())
                    now_time = time.strftime("%H%M%S", time.localtime())
                    file_dir = '/opt/socket/'+now_date
                    if not os.path.exists(file_dir):
                        os.makedirs(file_dir)
                    file_path = file_dir+'/'+now_time+'.txt'
                    f = open(file_path , 'wb')
                    f.write(bytes(str2, 'utf-8'))
                    f.close()
                    print('save in', file_path)
        cs.close()
except:
    print("Unexpected error:", sys.exc_info())