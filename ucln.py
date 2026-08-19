def gcd(a,b):
    while b!=0:
       a,b = b,a%b
    return a
if __name__ == "__main__":
    a = int(input())
    b = int(input())
    ucln = gcd(a,b)
    print(ucln)