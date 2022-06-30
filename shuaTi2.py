# 给定一个数字，平分2分，如果不够分，可以+1 或-1
# 经过x 次以后这个数变成1.
# 最少要经过多少次操作？
# 注释：  +1，-1，平分各自算一次操作。
 
# '''
# return action , list of actions.
# '''
def getV(n) -> int:

    n= int(n)
    if n==1:
        return 0 , [n,]
    else:
        if n % 2 == 0:
            v,lst1 = getV(n/2)
            lst1.append(n)
            return v+1,lst1
        else:
            ret1,lst1  = getV((n-1)/2)
            ret2 ,lst2 = getV((n+1)/2)
            if ret1 < ret2:
                lst1.append(n-1)
                lst1.append(n)
                return ret1+2,lst1
            else:
                lst2.append(n+1)
                lst2.append(n)
                return ret2+2,lst2

def main():
    n2=23
    n,lstv= getV(n2)
    print('Need action :',n2, n ,lstv)

    for n2 in range(2,100):
        n,lstv= getV(n2)
        print('Need action :',n2, n ,lstv)

if __name__ == "__main__":
    main()
    

