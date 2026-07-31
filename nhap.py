a = str(input())
tong_ki_tu = len(a)
print(tong_ki_tu)
#in ra ki tu dau tien và ki tu cuoi cung
print(a[0])
print(a[-1])
#chuỗi đảo ngược
print(a[::-1])
b = str(input())
if b in a:
    print("Có")
else:
    print("Không")
    