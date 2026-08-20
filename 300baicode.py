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
def prime(n):
    if n <=1: return False
    for i in range(2, int(n**0.5)+1):
        if n%i == 0: return False
    return True
def print_prime():
    for i in range(1,101):
        if prime(i): 
            print(i, end=" ")
def them_queue():
    q= []
    for item in input().split():
        q.append(int(item))
    line2 = input().split()
    x = int(line2[0])
    k = int(line2[1])
    n = len(q)
    if k<0 : k=0
    if k>=n : k=n
    for i in range(k):
        first_val = q.pop(0)
        q.append(first_val)
    q.append(x)
    for i in range(n-k):
        first_val = q.pop(0)
        q.append(first_val)
    res = []
    while len(q)>0:
        res.append(str(q.pop(0)))
    print(" ".join(res))
def xoa_queue():
    q = []
    for item in input().split():
        q.append(int(item))
    x = int(input())
    n =len(q)
    for i in range(n):
        val = q.pop(0)
        if val !=x:
            q.append(val)
    res = []
    while len(q)>0:
        res.append(str(q.pop(0)))
    print(" ".join(res))
if __name__ == "__main__":
    ket_qua = xoa_queue()
    print(ket_qua)
        

