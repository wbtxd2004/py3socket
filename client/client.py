#!/usr/bin/python3
# 文件名：client.py

# 导入 socket、sys 模块
import socket
import sys
import struct

#将16进制数据当做字节流传递
def dataSwitch(data):
    str1 = ''
    str2 = b''
    data = data.replace(' ','')
    while data:
        str1 = data[0:2]
        s = int(str1,16)
        x = struct.pack('B',s)
        # print(x)
        str2 += x
        # str2 += struct.pack('B',s)
        data = data[2:]
    return str2

if __name__ == "__main__":
    # 创建 socket 对象"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    # host = socket.gethostname()
    host = '47.104.170.183'
    # 设置端口号
    port = 9999
    # 连接服务，指定主机和端口
    client.connect((host, port))
    while True:
        data = input(">:")
        if not data:
            break
        if data == "00":
            break
        client.send(dataSwitch(data))
        data_r = client.recv(1024)
        # data_rr = client.recv(1024)
        print(data_r)
        # if not data_r:
        #     break
        # print(data_r)
        # break
    client.close()
    # B1C2FF82
    #11 13 55 aa 01 00 00 01 00 00 00 1e 00 00 00 12 06 01 0a 00 00 78 fd 4e 03 00 00 69 01 ce
