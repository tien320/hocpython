arr = [1, 2, 3, 4, 5, 6, 7]
k = 3
#Hãy xoay vòng danh sách sang phải $k$ bước (các phần tử ở cuối dịch chuyển lên đầu).
arr = arr[-k:] + arr[:-k]
print(arr)