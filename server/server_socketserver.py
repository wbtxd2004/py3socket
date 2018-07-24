#!/usr/bin/python3
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys
import struct
import time
import os
from socketserver import BaseRequestHandler,ThreadingTCPServer
import threading
from datetime import datetime
import binascii

def creatdir(device_no,measure_times):
    file_dir = "/opt/socket/"+device_no+"/"+measure_times
    if os.path.exists(file_dir):
        return file_dir
    else:
        os.makedirs(file_dir)
        return file_dir

def creatpicdir(device_no,measure_times):
    file_dir = "/opt/socket/"+device_no+"/"+measure_times+"/pic"
    if os.path.exists(file_dir):
        return file_dir
    else:
        os.makedirs(file_dir)
        return file_dir
class Handler(BaseRequestHandler):
    def handle(self):
        try:
            address, pid = self.client_address
            print('%s connected!'%address)
            count = 0
            while True:
                # 接收数据
                ra = self.request.recv(1024)
                if len(ra)>0:
                    cur_thread = threading.current_thread()
                    # 接收的原始数据
                    # print("raw:", ra)
                    data_all = binascii.b2a_hex(ra)[0:]
                    print("data:", data_all)
                    # 数据头部分
                    data_head = ra[0:15]
                    # 数据正文部分
                    data_body = ra[15:]
                    # print('head:',data_head)
                    # print('body', data_body)
                    # 返回数据部分
                    data_back = data_head
                    self.request.sendall(data_back)
                    # 发送数据长度
                    data_len_rec = data_all[24:26]+data_all[22:24]
                    data_len_rec = int(data_len_rec, 16)
                    # 接收数据长度
                    data_len_all = len(data_all)/2-15
                    # 测量时间-全局变量
                    measure_date =""
                    measure_time =""
                    if data_len_rec != data_len_all:
                        print("data not match")
                        #设置数据不匹配的反向控制
                        print("rec:", data_len_rec)
                        print("all;", data_len_all)
                    else:
                        # 设备号
                        device_no = int(data_all[10:12]+data_all[8:10],16)
                        print('device no:', device_no)
                        # 数据类型
                        device_type = data_all[12:14]
                        # device_type = int(data_all[12:14], 16)
                        # 测量次数
                        measure_times = int(data_all[20:22] + data_all[18:20] + data_all[16:18] + data_all[14:16], 16)
                        print("measure times :", measure_times)
                        file_dir = creatdir(str(device_no), str(measure_times))
                        if device_type == b'00':
                            # 存储设备运行数据文件
                            file_name = "device_operate_data"
                            file_path = file_dir + '/' + file_name
                            f = open(file_path, 'w')
                            print('设备运行数据')
                            f.write("设备运行数据\n")
                            # 测量时间
                            measure_time_year = str(2000 + int(data_all[30:32], 16)).zfill(4)
                            measure_time_month = str(int(data_all[32:34], 16)).zfill(2)
                            measure_time_day = str(int(data_all[34:36], 16)).zfill(2)
                            measure_time_hour = str(int(data_all[36:38], 16)).zfill(2)
                            measure_time_minute = str(int(data_all[38:40], 16)).zfill(2)
                            measure_time_second = str(int(data_all[40:42], 16)).zfill(2)
                            measure_date = measure_time_year+"_"+measure_time_month+"_"+measure_time_day
                            measure_time = measure_time_hour+"_"+measure_time_minute+"_"+measure_time_second
                            print("measer date: %s %s"%(measure_date, measure_time))
                            measure_date_save = "测量时间"+measure_date+measure_time
                            f.write(measure_date_save)
                            f.write('\n')
                            # 三轴角度
                            RollL = int(data_all[42:44],16)
                            RollH = int(data_all[44:46], 16)
                            PitchL = int(data_all[46:48], 16)
                            PitchH= int(data_all[48:50], 16)
                            YawL = int(data_all[50:52], 16)
                            YawH = int(data_all[52:54], 16)
                            Roll = ((RollH<<8)|RollL)/32768*180
                            Pitch = ((PitchH<<8)|PitchL)/32768*180
                            Yaw = ((YawH<<8)|YawL)/32768*180
                            print("姿态",Roll,Pitch,Yaw)
                            zitai_date_save = "姿态",Roll,Pitch,Yaw
                            # f.write(zitai_date_save)
                            # 三轴磁场
                            HxL = int(data_all[54:56], 16)
                            HxH = int(data_all[56:58], 16)
                            HyL = int(data_all[58:60], 16)
                            HyH = int(data_all[60:62], 16)
                            HzL = int(data_all[62:64], 16)
                            HzH = int(data_all[65:66], 16)
                            Hx = ((HxH<<8)|HxL)
                            Hy = ((HyH<<8|HyL))
                            Hz = ((HzH<<8)|HzL)
                            print("磁轴：", Hx, Hy, Hz)
                            # 经纬度
                            Lon0 = int(data_all[66:68], 16)
                            Lon1 = int(data_all[68:70], 16)
                            Lon2 = int(data_all[70:72], 16)
                            Lon3 = int(data_all[72:74], 16)
                            Lat0 = int(data_all[74:76], 16)
                            Lat1 = int(data_all[76:78], 16)
                            Lat2 = int(data_all[78:80], 16)
                            Lat3 = int(data_all[80:82], 16)
                            Lon = (Lon3<<24)|(Lon2<<16)|(Lon1<<8)|Lon0
                            Lon_dd = round(Lon/10000000)
                            Lon_mm = (Lon%10000000)/100000
                            print("经度", Lon/10000000)
                            Lat = (Lat3<<24)|(Lat2<<16)|(Lat1<<8)|Lat0
                            print("纬度", Lat/10000000)
                            # 卫星定位精度
                            SNL = int(data_all[82:84], 16)
                            SNH = int(data_all[84:86], 16)
                            PDOPL = int(data_all[86:88], 16)
                            PDOPH = int(data_all[88:90], 16)
                            HDOPL = int(data_all[90:92], 16)
                            HDOPH = int(data_all[92:94], 16)
                            VDOPL = int(data_all[94:96], 16)
                            VDOPH = int(data_all[96:98], 16)
                            SN = ((SNH<<8|SNL))
                            PDOP = ((PDOPH<<8|PDOPL))/100
                            HDOP = ((HDOPH<<8)|HDOPL)/100
                            VDOP = ((VDOPH<<8)|VDOPL)/100
                            print("卫星数量：", SN)
                            print("位置定位精度",PDOP)
                            print("水平定位精度",HDOP)
                            print("垂直定位精度",VDOP)
                            # 温度
                            TL = int(data_all[98:100], 16)
                            TH = int(data_all[100:102], 16)
                            T = ((TH<<8)|TL)/100
                            print("温度：", T)
                            # 湿度
                            humidity = int(data_all[102:104],16)
                            print("湿度:", humidity)
                            # 电量
                            battery = int(data_all[104:106],16)
                            print("电量:",battery)
                            # 故障代码
                            error_code = data_all[106:108]
                            if error_code == b'00':
                                print("zhengchang")
                            elif error_code == b'01':
                                print("机械故障")
                            elif error_code == b'02':
                                print("存储故障")
                            elif error_code == b'03':
                                print("定位故障")
                            elif error_code == b'04':
                                print("姿态故障")
                            elif error_code == b'05':
                                print("通信故障")
                            elif error_code == b'06':
                                print("传感器故障")
                            elif error_code == b'07':
                                print("摄像头故障")
                            elif error_code == b'08':
                                print("电源故障")
                            elif error_code == b'09':
                                print("其他故障")
                            else:
                                print("未知故障")
                            f.close()
                            print('save in', file_path)
                        elif device_type == b'01':
                            print("no 1 sensor")
                            # 存储传感器文件
                            file_name = "sensor_data_" +bytes.decode(device_type)
                            file_path = file_dir + '/' + file_name
                            f = open(file_path, 'wb')
                            f.write(data_body)
                            f.close()
                            print('save in', file_path)
                        elif device_type == b'02':
                            print("no 2 sensor")
                            # 存储传感器文件
                            file_name = "sensor_data_"  + bytes.decode(device_type)
                            file_path = file_dir + '/' + file_name
                            f = open(file_path, 'wb')
                            f.write(data_body)
                            f.close()
                            print('save in', file_path)
                        elif device_type == b'03':
                            print("no 3 sensor")
                            # 存储传感器文件
                            file_name = "sensor_data_" + bytes.decode(device_type)
                            file_path = file_dir + '/' + file_name
                            f = open(file_path, 'wb')
                            f.write(data_body)
                            f.close()
                            print('save in', file_path)
                        elif device_type == b'04':
                            pic_order = int(data_all[26:28], 16)
                            pic_number = int(data_all[28:30], 16)
                            print("pic data, order %d;number %d"%(pic_order,pic_number))
                            # 存储图片文件
                            pic_dir = creatpicdir(str(device_no), str(measure_times))
                            pic_name = "pic_" + str(pic_order)
                            pic_path = pic_dir + '/' + pic_name
                            f = open(pic_path, 'wb')
                            f.write(data_body)
                            f.close()
                            print('save in', pic_path)
                            pic_list = os.listdir(pic_dir)
                            pic_list.sort(key=lambda x:int(x[4:]))
                            file_numbers = len(pic_list)
                            if file_numbers == pic_number:
                                new_pic_name = "pic_" + str(device_no) + "_" + str(measure_times)
                                new_pic = open(file_dir + '/' + new_pic_name, 'wb')
                                pic_data = b''
                                for i in pic_list:
                                    f = open(pic_dir+'/'+i,'rt')
                                    pic_data += f.read()
                                    f.close()
                                new_pic.write(pic_data)
                                new_pic.close()
                        print('back', data_back)
                        print('len_rec',data_len_rec)
                        print('len_all',data_len_all)
                        # self.request.sendall(data_back)
                        # str1 = b''
                        # str2 = ''
                        # str3 = ''
                        # str_back = ''
                        # str_back_2 = b''
                        # str_back_3 = ra[0:15]
                        # len_re = ''
                        # while ra:
                        #     str1 = ra[0:1]
                        #     x = struct.unpack('B', str1)
                        #     str_back_2 += bytes(hex(x[0]), 'utf-8')
                        #     y = hex(x[0])[2:]
                        #     if len(y) == 1:
                        #         str2 += '0' + y + ' '
                        #         if count < 15:
                        #             str_back += '0' + y + ' '
                        #     else:
                        #         str2 += y + ' '
                        #         if count < 15:
                        #             str_back += y + ' '
                        #     str3 += hex(x[0])
                        #     ra = ra[1:]
                        #     if count == 11:
                        #         len_re = y
                        #     elif count == 12:
                        #         len_re = y + len_re
                        #     count = count + 1
                        # print("back:", str_back_3)
                        # self.request.sendall(str_back_3)
                        # # cs.send(bytes(str_back))
                        # data_len = len(str2.replace(' ', '')) / 2 - 15
                        # re_len = int(len_re, 16)
                        # print('data_len:', data_len)
                        # print('re_len:', re_len)
                        # if data_len != re_len:
                        #     print('data not match')
                        #     # cs.send(bytes(re_len, 'utf-8'))
                        #     break
                        # else:
                        #     # print(data_len)
                        #     # print(re_len)
                        #     now_date = time.strftime("%Y%m%d", time.localtime())
                        #     now_time = time.strftime("%H%M%S", time.localtime())
                        #     file_dir = '/opt/socket/' + now_date
                        #     if not os.path.exists(file_dir):
                        #         os.makedirs(file_dir)
                        #     file_path = file_dir + '/' + now_time + '.txt'
                        #     f = open(file_path, 'wb')
                        #     f.write(bytes(str2, 'utf-8'))
                        #     f.close()
                        #     print('save in', file_path)
                else:
                    print("no data")
                    break

        except Exception:
            print('error')
            self.close()
            sys.exit()

if __name__ == '__main__':
    # 获取本地主机名
    host = socket.gethostname()
    # host = '127.0.0.1'
    port = 9999
    ADDR = (host, port)
    server = ThreadingTCPServer(ADDR, Handler)
    print('listening')
    server.serve_forever()
    print(server)