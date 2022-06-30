from ftplib import FTP

'''
通过 命令行实现FTP 功能
'''

Host = "10.42.222.202"
Port=21
user = "K0509462"
pwd = 'lwplwp123'
helpstring = '''
h help
ls list
cd xxx change remote dir
pwd current remote dir
get download file.
put upload a file.
d   delete a remote file.
df  delete a remote folder.
q exit ftp interface.
'''

input1 = input("input Host addres [10.42.222.202]")
if  input1:
    Host=input1
input1 = input("input user [K0509462]")
if  input1:
    user=input1
input1 = input("input password [lwplwp123]")
if  input1:
    pwd=input1

f=FTP(Host)
f.port=Port
f.login(user,pwd) #f.login() this means anonymous
f.debugging= 0
f.encoding = 'utf-8'
w=f.getwelcome()
print(w)
print(helpstring)

while (True):
    input1 = input('>')
    cmd=""
    cmdAll=''
    if input1:
        cmd = input1.split()[0]
        cmdAll=input1
    if cmd=='h':
        print(helpstring)
    if cmd =='q':
        f.quit()
        break
    if cmd == 'ls':
        lst=f.nlst(f.pwd())
        #print(lst)
        for var in lst:
            print(var)
    if cmd == 'pwd':
        print(f.pwd())
    if cmd =='cd':
        path1= cmdAll[2:].strip()
        try:
            f.cwd(path1)
            print(f.pwd())
        except Exception as ex:
            print('Error: ' , ex)

    if cmd == 'get':
        # f.retrbinary('RETR %s' % '/Work/WP_Li/app_icon2.zip' ,open( r'/vault/ftpout.tmp','wb').write )
        # print('download finished.')
        input1 =  input('input remote file :')
        if input1:
            rfile = input1
        else:
            print("no remote file . cancel action.")
            continue
        input1 =  input('input Local file with full path:')
        if input1:
            lfile = input1
        else:
            print("no Local file . cancel action.")
            continue
        try:
            f.retrbinary('RETR %s' % rfile ,open( lfile,'wb').write )
            print('download finished.')
        except Exception as e:
            print("Error:",e) 
    if cmd == 'put': 
        input1 =  input('input remote file :')
        if input1:
            rfile = input1
        else:
            print("no remote file . cancel action.")
            continue
        input1 =  input('input Local file with full path:')
        if input1:
            lfile = input1
        else:
            print("no Local file . cancel action.")
            continue
        try:
            f.storbinary('STOR %s' % rfile , open( lfile,'rb')  )
            print('upload finished.')
        except Exception as e:
            print("Error:",e) 
    if cmd =='d':
        input1 =  input('input remote file :')
        if input1:
            rfile = input1
        else:
            print("no remote file . cancel action.")
            continue
        try:
            f.delete(rfile)
            print('delete finished.')
        except Exception as e:
            print("Error:",e) 
    if cmd =='df':
        input1 =  input('input remote file :')
        if input1:
            rfile = input1
        else:
            print("no remote file . cancel action.")
            continue
        try:
            f.rmd(rfile)
            print('delete finished.')
        except Exception as e:
            print("Error:",e) 

# f.quit()
print(" FTP finished.".center(40,'-'))


