def sinhvien(sinh_vien,ten):
    if ten in sinh_vien:
        return True
if __name__ == "__main__":
    n =int(input())
    ten = input()
    sinh_vien =[]
    for i in range(n):
        sinh_vien.append((input()))
    print(sinhvien(sinh_vien,ten))
    
    