def twosum(nums,target):
    n = len(nums)
    for i in range(n):
        for j in range(i+1,n):
            if nums[i] + nums[j] == target:
                return [i,j]
    return []
if __name__ == "__main__":
    nums = list(map(int,input().split()))
    target = int(input())
    ket_qua = twosum(nums,target)
    print(ket_qua)