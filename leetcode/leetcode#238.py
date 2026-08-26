def array(nums):
    n = len(nums)
    res = [1]*n
    left =1
    for i in range(n):
        res[i] = left
        left *= nums[i]
    right =1 
    for i in range(n-1,-1,-1):
        res[i] *= right
        right *= nums[i]
    print(res)
if __name__ == "__main__":
    nums = [1,2,3,4]
    print(array(nums))
