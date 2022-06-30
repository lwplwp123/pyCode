from time import ctime
from threading import Thread
import re
from urllib.request import urlopen
import atexit

url= r'https://www.apple.com.cn'
Regex = re.compile(r'"url": "(.*?)"')

def getData():
    page = urlopen(url)
    data = page.read()
    page.close()
    return data
def main():
    get= getData()
    # print(get)
    # print(Regex.findall(get))
    s0= re.findall(Regex,get)
    for s in s0:
        print( 'value:  '+ s)

@atexit.register
def atexit1():
    print ('all exist ...')


if __name__ == '__main__':
    main()
 