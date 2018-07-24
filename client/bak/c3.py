#!/usr/bin/python3
# 文件名：client.py

# 导入 socket、sys 模块
import socket
import sys

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
    cmd = input(">>>:").strip()
    if len(cmd) == 0: continue
    client.send(cmd.encode("utf-8"))
    cmd_res_size = client.recv(1024)  # 接收命令的长度
    print("命令结果大小：", cmd_res_size.decode())
    recevied_size = 0  # 接收客户端发来数据的计算器
    recevied_data = b''  # 客户端每次发来内容的计数器
    while recevied_size < int(cmd_res_size.decode()):  # 当接收的数据大小 小于 客户端发来的数据
        cmd_res = client.recv(1024)
        recevied_size += len(cmd_res)  # 每次收到的服务端的数据有可能小于1024，所以必须用len判断
        recevied_data += cmd_res
    else:
        print(recevied_data.decode("utf-8", "ignore"))
        print("cmd res receive done ....", recevied_size)
    client.close
