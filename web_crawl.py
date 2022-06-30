import os
import sys
import urllib.parse ,urllib.request
import ssl
import re 


dicAllDownload =[]


def downloadURL(url1,pathRoot):
    url1=re.sub(r'/./',r'/',url1)
    if dicAllDownload.count(url1): 
        return
    else:
        dicAllDownload.append(url1)

    try:
        cont=ssl._create_unverified_context()
        mainbody=urllib.request.urlopen(url1,context=cont)
        bbody=mainbody.read()
        try:
            mainbody = bbody.decode('utf-8')
        except:
            mainbody = bbody.decode('gb2312')

    except  os.error as N:
        print('Can not open URL:' , url1)
        print(N)
        return 

    parseURL = urllib.parse.urlsplit(url1)
    hostName= parseURL.netloc
    FileName = re.split('/',parseURL.path)[-1]
    currPath =  parseURL.path[0: len(parseURL.path) - len(FileName)] #/Path/path2
    urlParentPath = url1[0:len(url1) - len(FileName)]
    urlRoot = parseURL.scheme + "://" + parseURL.netloc + "/"
    if not urlParentPath.endswith('/'): urlParentPath +='/'
    if FileName =='': FileName ='index.html'
    if currPath =='': currPath ='/'

    # print(mainbody)

    path2  = pathRoot+ currPath

    #create the folder. 
    if os.path.exists(path2):
        print('output folder exist',path2)
    else:
        os.makedirs(path2)
 

    subURLs=re.findall('href="(.*?)"',mainbody)
    for aUrl in subURLs:
        aUrl=str(aUrl)
        if aUrl.count(r'://')  and not aUrl.count(r'://%s/'% hostName ) :
            print('by pass ' , aUrl)
        elif aUrl.startswith(r'#') or aUrl =='':
            print('by pass of #' ,aUrl)

        else:
            print( 'will download :' ,aUrl)
            print( '      '+parseURL.scheme +'://'+ parseURL.netloc +'/' + aUrl )
            
            if re.findall(r'://' ,aUrl):
                mainbody = re.sub( f'{aUrl}' , pathRoot +changeAspxName(urllib.parse.urlsplit(aUrl).path) ,mainbody)
                

                downloadURL(aUrl,pathRoot)  # 递归调用所以的链接。
            elif aUrl.startswith('/') :
                mainbody = re.sub( f'{aUrl}' , pathRoot +changeAspxName(urllib.parse.urlsplit(aUrl).path) ,mainbody)
                downloadURL( urlRoot+ aUrl[1:],pathRoot)  # 递归调用所以的链接。
            else:
                mainbody = re.sub( f'{aUrl}' , currPath[1:] +changeAspxName(urllib.parse.urlsplit(aUrl).path) ,mainbody)
                downloadURL( urlParentPath+ aUrl,pathRoot)  # 递归调用所以的链接。

 #save to a file.
    fname = os.path.join(path2, changeAspxName( FileName))
    with open(fname,'w') as f:
        f.write(mainbody)

def changeAspxName(urlP:str)->str:
    '''give a url , if end with aspx, return xx.html'''
    if urlP.lower().endswith('.aspx'):
        return urlP[0:len(urlP)-5] + '.html'
    elif urlP.lower().endswith('.asp'):
        return urlP[0:len(urlP)-4] + '.html'
    else:
        return urlP


if __name__ == '__main__':
    mainurl = 'http://www.baidu.com' #input('please input a URL:')
    mainurl = 'http://10.42.24.213' #input('please input a URL:')
    # mainurl = 'http://10.42.24.213/Account/./../Styles/register.css' #input('please input a URL:')
    newP= os.path.dirname(__file__) 
    newP = os.path.join(newP,'web_crawlOut')
    dicAllDownload.clear()
    downloadURL(mainurl,newP)
    dicAllDownload.clear()


