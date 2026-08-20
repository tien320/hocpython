def contain_duplicate(nums):
    nums.sort()
    n =len(nums)
    for i in range(n-1):
        if nums[i] == nums[i+1]: return True
    return False
if __name__ == "__main__":
    nums = list(map(int,input().split()))
    ket_qua = contain_duplicate(nums)
    print(ket_qua)
