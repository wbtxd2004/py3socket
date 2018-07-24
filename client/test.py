import sys
x=10
# print(chr(32))
# print(len(hex(x)[2:]))
# print(int('0x014f',16))
# str = '11 13 55 aa 01 00 00 01 00 00 00 4f 00 00 00 12 06 01 0a 00 00 78 fd 4e 03 00 00 69 01 ce 01 14 00 f0 d7 6a 45 40 eb cb 17 0a 00 34 02 45 02 18 01 4d 07 37 64 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
# str_1 = '12 06 01 0a 00 00 78 fd 4e 03 00 00 69 01 ce 01 14 00 f0 d7 6a 45 40 eb cb 17 0a 00 34 02 45 02 18 01 4d 07 37 64 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
# str_2 = str.encode('ascii')
# str_3 = str_1.replace(' ','')
# print(len(str_3)/2)
# print(str_2)
# print(chr(10))
# y = list(str)
# print(y)
# print(len(y))
# len = sys.getsizeof(str_2)
# print(len)
# print(len(str))
# print(int('14f',16))
str = 'fd'
xx = int(str, 16)
yy = ((xx<<8)|120)
print(yy)
# print(type(str))
print(int(str, 16))
# print(len(hex(1)[2:]))
# print(4|7)
dd_list = ["pic_01","pic_1","pic_2","pic_10","pic_3","pic_22"]
# dd_list = ["01","1","2","10","3","22"]
print(dd_list)
dd_list.sort(key=lambda x:int(x[4:]))
print(dd_list)
print(sorted(dd_list))