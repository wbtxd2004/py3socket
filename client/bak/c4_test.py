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
        # s = int(str1,16)
        s = chr(str1, 16)
        x = struct.pack('B',s)
        print(x)
        str2 += x
        # str2 += struct.pack('B',s)
        data = data[2:]
    return str2

if __name__ == "__main__":
    data = input(">:")
    print(data)
    # if not data:
    #     break
    # if data == "00":
    #     break
    ssss = dataSwitch(data)
    print(sys.getsizeof(data))
    print(type(data))
