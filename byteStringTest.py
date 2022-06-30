
byte1 =b'abc'
byte1=b'\x31\x32\x33\x11'
str1 = byte1.decode('utf-8')
str2=byte1
byte2 = str1.encode('utf-8')
print(byte1)
print (str1)
print (str2)
print(byte2)
print(repr(byte1))
str2=f'{byte1!r}'
print(str2)
# print(bytes.fromhex(str1))