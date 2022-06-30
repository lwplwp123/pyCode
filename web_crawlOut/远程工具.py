import os
import re,json,requests 

'''
这个工具失败了， 不提供可视化界面太不方便。
'''
strPrompot='''
请输入你要的操作： 然后依据提示操作。
1. reboot 一些电脑。
2. shutdown 一些电脑
3. 远程桌面 一些电脑
'''

def getSelect(litX:list)->list:
    idx=0
    for ax in litX:
        print(idx,ax)
        idx+=1

    inp=''
    
    while True:
        inp = input('please select index or * (All) , other key for filter:')
        if inp.isnumeric() and int(inp) < len(litX) :
            return [litX[int(inp)]]
        elif inp=='*' :
            return litX
        else:
            print(litX)
            [ print(x) for x in litX if x.count(inp) ]


def findIPs():
    resp = requests.request("GET",'http://10.42.24.213/gh/gh_Console.aspx?c=getlinelist&product=d63')
    json1 = json.loads( resp.text)
    # lst = [x['Line'] for x in json1 ]
    # list2= getSelect(lst)
    # lst= sorted(json1,key=lambda x : x['Line'].split('-')[2])

    json1.sort(key=lambda x: x['Line'].split('-')[2]  )
    for dic in json1:
        print(dic)
        # print (dic['Line'])


findIPs()

inp=input(strPrompot)

if inp == '1':
    print('reboot ')
elif inp =='2':
    print('shutdown')
elif inp =='3':
    print ('remote vnc')

