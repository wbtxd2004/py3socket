#!/usr/bin/python3
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys
import struct
import time
import os
import threading
from datetime import datetime

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取本地主机名
host = socket.gethostname()
# host = '127.0.0.1'
port = 6666
# true = True
def rec(cs):
    # global true
    while True:
        # cs.send(b"begin")
        ra = cs.recv(1024)
        # cs.send(ra)
        # cs.send(b"over")
        # print(ra)
        count = 0
        if not ra:
            print("no data")
            break
        else:
            print("raw:", ra)
            str1 = b''
            str2 = ''
            str3 = ''
            str_back = ''
            str_back_2 = b''
            str_back_3 = ra[0:15]
            data = ra[16:]
            print(data)
            len_re = ''
            device_num =''
            while ra:
                str1 = ra[0:1]
                x = struct.unpack('B', str1)
                str_back_2 += bytes(hex(x[0]), 'utf-8')
                y = hex(x[0])[2:]
                if len(y) == 1:
                    str2 += '0' + y + ' '
                    if count < 15:
                        str_back += '0' + y + ' '
                else:
                    str2 += y + ' '
                    if count < 15:
                        str_back += y + ' '
                str3 += hex(x[0])
                ra = ra[1:]
                if count == 11:
                    len_re = y
                elif count == 12:
                    len_re = y + len_re
                count = count + 1
            print("back:", str_back_3)
            cs.send(str_back_3)
            # cs.send(bytes(str_back))
            data_len = len(str2.replace(' ', '')) / 2 - 15
            re_len = int(len_re, 16)
            print('data_len:', data_len)
            print('re_len:', re_len)
            print('raw-2:', str2)
            if data_len != re_len:
                print('data not match')
                # cs.send(bytes(re_len, 'utf-8'))
                break
            else:
                # print(data_len)
                # print(re_len)
                dt = datetime.now()
                now_date = dt.strftime("%Y%m%d")
                now_time = dt.strftime("%H%M%S%f")
                file_dir = '/opt/socket/' + now_date
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                file_path = file_dir + '/' + now_time + '.txt'
                f = open(file_path, 'wb')
                f.write(bytes(str2, 'utf-8'))
                f.close()
                print('save in', file_path)
    cs.close()

try:
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
        trd = threading.Thread(target=rec, args=(cs,))
        trd.start()
except Exception as e:
    print('error:', e)
    serversocket.close()
    sys.exit()