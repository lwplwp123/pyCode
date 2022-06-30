import json
import pprint


Books = {
    '0123456':{
        'title':'this is title',
        'editor':'tom',
        'year':2013
    },
    '212458':{
        'title':'this is title2',
        'editor':'Jerry',
        'year': 2019
    },
    '026599':{
        'title':'this is title4',
        'authors':'Grow',
        'year':2023
    }
}

a= dict( zip('abcde','123'))
jStr=json.dumps(a)

print('\r\n\r\n=============begin')
print('row dictionary:' )
print(Books)

print('++++++++++pretty print result')
pprint.pprint(Books)

print('=====json string')
print(json.dumps(Books))


print('++++++++++pretty print dumps')
pprint.pprint(json.dumps(Books,indent=4))


print(jStr)

dic1= { 'k1':'v1','k2':'v2' , 'k3':'v4'}
print('')

for k in dic1:
    print(k)

a='B\\abc'
print(a.islower())
print(max(a))
#print(ord(a))
print(chr(66))
print(oct(9))

a= hex(18)
v= int(a,16)
print (a,v)

a= -4
b=0xFF
v= hex(a+b+1)
print(a,b,v)

b = bin(a)
print(a,f'0000{b}****')



