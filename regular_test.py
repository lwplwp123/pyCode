import re

source1 = 'he is 28 years, and she is 18 years old.'
ret =re.findall('(\d+)',source1)
print(ret)

ret = re.match('.*?(\d+)',source1)
if ret !=None: print('match funciton    ',ret.group(0))

ret = re.sub('(\d+)' , r'(\1)' ,source1)
print ('for sub function : ',ret)

m = re.match('.*?(\d+)', 'ab 123 456') # 两个子组
if m !=None: print(m.group()) # 完整匹配


m= re.search('(\d+)' , source1)  #search can only return the first match.
if m:
    print('search   ', source1,m)


source2= '''address1:http://www.pan.com/abcew.aspx
address2:http://www.pfew.com/new.aspx
address3:http://www.fff.com/third.aspx
'''

a='\\1.html'
b=r'\1.html'

b2=f'{b}'
b3=rf'{b}'
print('b2/b3'  ,b2,b3)
out2 = re.sub(r'(www\..*\.com/.*)\.aspx' ,f'{b}',source2)
print(out2)


c=r'(www\..*\.com/.*)\.aspx' 
d='(www\..*\.com/.*)\.aspx' 

print(a,b,c,d)