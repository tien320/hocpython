def taxi(n):
    if n<0 : return False
    elif n<=1 : 
        return n*12000
    elif n<=30 :
            return 12000 + (n-1)*10000
    else:
        return n*12000 + 29*10000 + (n-30)*9000
def gcd(a,b):
    while b!=0:
       a,b = b,a%b
    return a
if __name__ == "__main__":
    n = int(input())
    a = int(input())
    b = int(input())
    ket_qua = taxi(n)
    print(ket_qua)
    ucln = gcd(a,b)
    print(ucln)
        

