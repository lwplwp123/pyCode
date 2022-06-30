# coding:utf-8


#sample 1 , old way.
# import urllib.request

# url='http://127.0.0.1:8088'
# # url="http://10.42.24.213"
# data ='this is data.'

# a=urllib.request.urlopen(url,data=data.encode() ,timeout=10  )
# ret= a.read().decode()

# # try:
# #     a=urllib.request.urlopen(url,data=data.encode() ,timeout=10)
# #     ret= a.read()
# # except  Exception as  exa:
# #     print('exception....')
# #     ret= "\r\n".join( exa.args)

# print(ret)
 

#sample 2 , it was said , this is a new way.
import requests  

# response = requests.get("http://www.baidu.com/")
# 也可以这么写
# response = requests.request("get", "http://www.baidu.com/")

kw = {'wd':'长城'}
 
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
 
# # params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
# response = requests.get("http://127.0.0.1:8080", params = kw, headers = headers)
# # 查看响应内容，response.text 返回的是Unicode格式的数据
# print (response.text)
 
# # 查看响应内容，response.content返回的字节流数据
# print (response.content)
 
# # 查看完整url地址
# print (response.url)
 
# # 查看响应头部字符编码
# print (response.encoding)
 
# # 查看响应码
# print (response.status_code) 

# a= requests.get("http://127.0.0.1:8080",headers={"Content-Type":"application/json"},data="get...data...")
# print(a.cookies)
# print(a.content)


a= requests.post("http://127.0.0.1:8080",headers={"Content-Type":"application/json"},data="get...data...")
print(a.cookies)
print(a.content)


# class getheader():      
#     @staticmethod     
#     def session():          #封装测试数据         
#         data = 'test data'         
#         url = ConnUrl.getUrl ()         
#         url = url+'200000'     #设置header         
#         header = {'content-type':'application/octet-stream'}     #post请求         
#         post = requests.post(url, data=data, headers=header)     #通过split函数切割返回数据，获得session         
#         jsessionid = post.headers['Set-Cookie'].split(';')[0]         
#         return jsessionid

