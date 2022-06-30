# coding:utf-8

 
import os,re,sys
import datetime,traceback
import pipes,requests,json

# strCont = open('/vault/tmp.2','rb').read().decode('utf-8' , 'ignore')

# sn=re.findall('\n(.*?),T677,' ,strCont)
# sn= len(sn)>0 and sn[0] or 'nnn'
# print(sn) 
# ar=re.split(',',sn)
# print(ar)
print(3.8*1.1)


kw = {'c':'updateauditdate',
    'operateType':'updateauditdate',
    'stationId':'stationID',
    'auditDate':datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
    'expDate':datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
    'alertDate':datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
    'stationType': 'stationtype',
    'product':'product',
    'line':'line',
    'ip':'172.3.3.3'
    }
kwStr= json.dumps(kw)

response = requests.post('http://10.42.24.213/gh/gh_Console.aspx',data= kwStr, params = kw )
print(response.text)


'''
https://u.j-cc.cn/ojYa2l
https://u.j-cc.cn/bgXaW7
curl -X POST -H "Content-Type:application/json" -H "token:test" "http://172.30.60.14:8081/appApi/sysAudit/updateFixtureAudit"  -d  @/vault/p.txt
curl -X POST -H "Content-Type:application/json" -H "token:test" "http://172.30.70.161/appApi/sysAudit/updateFixtureAudit"  -d  @/vault/p.txt
curl -X POST "http://localhost:7200" -d ' { "Request": { "Command" : "QueryConfig",  "StationId": "LXKS_A03-3FP-11_2_ICHECK"}, "UUID": "11D3F39C-3516-4202-9B25-7B88F92135E3","Version": "1" } '
Serial Number: G2C820503NKJMW1AR
15:15:15.974 - INFO - InstantPudding Serial Number G2C820503NKJMW1AR is already stored
15:15:15.974 - INFO - GUI - Found Serial Number: G2C820503NKJMW1AR

'''